(() => {
  'use strict';

  const cards = document.querySelectorAll('[data-release-date]');
  const status = document.getElementById('release-status');
  const formatter = new Intl.DateTimeFormat('en', {
    timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit'
  });

  function isValidDate(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
    const parsed = new Date(`${value}T00:00:00Z`);
    return !Number.isNaN(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value;
  }

  function refresh() {
    const parts = formatter.formatToParts(new Date());
    const part = type => parts.find(item => item.type === type).value;
    const today = `${part('year')}-${part('month')}-${part('day')}`;
    let visible = 0;
    cards.forEach(card => {
      const releaseDate = card.dataset.releaseDate;
      const published = card.dataset.published === 'true';
      card.hidden = !(published && isValidDate(releaseDate) && releaseDate <= today);
      if (!card.hidden) visible += 1;
    });
    if (status) status.hidden = visible > 0;
  }

  refresh();
  window.setInterval(refresh, 60_000);
  window.addEventListener('pageshow', refresh);
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') refresh();
  });
})();
