const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const script = fs.readFileSync(path.join(root, 'release-schedule.js'), 'utf8');
const sections = [...html.matchAll(/<section\b([^>]*)>([\s\S]*?)<\/section>/g)];
function harness(instant, extras = []) {
  let now = instant;
  const cards = sections.map(([, attrs, body]) => ({
    dataset: {
      releaseDate: /data-release-date="([^"]*)"/.exec(attrs)?.[1],
      published: /data-published="([^"]*)"/.exec(attrs)?.[1]
    },
    hidden: /\bhidden\b/.test(attrs),
    href: /href="([^"]*)"/.exec(body)?.[1]
  })).concat(extras);
  const listeners = {};
  const status = { hidden: true };
  const document = {
    visibilityState: 'visible',
    querySelectorAll: selector => {
      assert.equal(selector, '[data-release-date]');
      return cards;
    },
    getElementById: id => { assert.equal(id, 'release-status'); return status; },
    addEventListener: (name, callback) => { listeners[name] = callback; }
  };
  const window = {
    setInterval: (callback, duration) => {
      assert.equal(duration, 60_000);
      listeners.interval = callback;
    },
    addEventListener: (name, callback) => { listeners[name] = callback; }
  };
  class Clock extends Date {
    constructor(...args) { super(...(args.length ? args : [now])); }
  }
  vm.runInNewContext(script, { document, window, Intl, Date: Clock });
  return {
    cards, status, document, listeners,
    setTime: value => { now = value; },
    visible: () => cards.filter(card => !card.hidden).map(card => card.href)
  };
}
const day2 = './2026-11-02/';
const day5 = './2026-11-05/';

test('every card starts hidden, has explicit release permission, and preserves its local link', () => {
  assert.equal(sections.length, 11);
  for (const [, attrs, body] of sections) {
    assert.match(attrs, /\bhidden\b/);
    assert.match(attrs, /data-published="true"/);
    assert.match(attrs, /data-release-date="\d{4}-\d{2}-\d{2}"/);
    const href = /href="([^"]*)"/.exec(body)[1];
    assert.ok(fs.existsSync(path.join(root, href, 'index.html')), href);
    const lesson = /<time datetime="([^"]*)"/.exec(body);
    if (lesson) assert.ok(attrs.includes(`data-release-date="${lesson[1]}"`));
  }
  assert.match(html, /\[hidden\]\{display:none!important\}/);
  assert.match(html, /<script src="\.\/release-schedule.js" defer>/);
  assert.match(html, /<noscript>/);
});

test('Korean midnight releases each lesson cumulatively', () => {
  assert.deepEqual(harness('2026-11-01T14:59:59Z').visible(), []);
  assert.equal(harness('2026-11-01T14:59:59Z').status.hidden, false);
  assert.deepEqual(harness('2026-11-01T15:00:00Z').visible(), [day2]);
  assert.deepEqual(harness('2026-11-04T14:59:59Z').visible(), [day2]);
  assert.deepEqual(harness('2026-11-04T15:00:00Z').visible(), [day2, day5]);
  assert.equal(harness('2026-11-04T15:00:00Z').status.hidden, true);
});

test('assignment and DB basics open on November 12, all by November 23', () => {
  const before12 = harness('2026-11-11T14:59:59Z').visible();
  assert.ok(!before12.includes('./assignments/short-url/'));
  assert.ok(!before12.includes('./shared/db-basics/'));
  const day12 = harness('2026-11-11T15:00:00Z').visible();
  assert.ok(day12.includes('./2026-11-12/'));
  assert.ok(day12.includes('./assignments/short-url/'));
  assert.ok(day12.includes('./shared/db-basics/'));
  assert.ok(harness('2026-11-13T15:00:00Z').visible().includes('./shared/db-basics/'));
  assert.equal(harness('2026-11-22T15:00:00Z').visible().length, 11);
});

test('future, withheld, missing-permission and invalid dates remain hidden', () => {
  const extras = [
    ['2026-11-02', 'false'], ['2026-11-02', undefined],
    ['2026-11-02', 'TRUE'], ['2026-02-30', 'true'],
    ['2026-2-02', 'true'], ['', 'true'], [undefined, 'true']
  ].map(([releaseDate, published]) => ({ dataset: { releaseDate, published }, hidden: false }));
  const page = harness('2026-11-02T00:00:00Z', extras);
  assert.ok(extras.every(card => card.hidden));
  assert.deepEqual(page.visible(), [day2]);
});

test('date calculation is independent of the system timezone', () => {
  const previous = process.env.TZ;
  try {
    for (const timezone of ['UTC', 'America/Los_Angeles', 'Asia/Seoul']) {
      process.env.TZ = timezone;
      assert.deepEqual(harness('2026-11-04T15:00:00Z').visible(), [day2, day5]);
    }
  } finally {
    if (previous === undefined) delete process.env.TZ;
    else process.env.TZ = previous;
  }
});

test('open pages refresh after midnight through timer, pageshow and visible tab events', () => {
  for (const event of ['interval', 'pageshow', 'visibilitychange']) {
    const page = harness('2026-11-04T14:59:59Z');
    page.setTime('2026-11-04T15:00:00Z');
    page.listeners[event]();
    assert.deepEqual(page.visible(), [day2, day5]);
  }
  const page = harness('2026-11-04T14:59:59Z');
  page.setTime('2026-11-04T15:00:00Z');
  page.document.visibilityState = 'hidden';
  page.listeners.visibilitychange();
  assert.deepEqual(page.visible(), [day2]);
  page.document.visibilityState = 'visible';
  page.listeners.visibilitychange();
  assert.deepEqual(page.visible(), [day2, day5]);
});
