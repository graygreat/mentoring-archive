"""Run local HTTP contract/restart checks against projects from build_examples.py.

Build the examples first. JAVA_HOME must point to Java 17.
Usage: python3 shared/rehearse_http.py --projects /tmp/course-examples
This uses isolated ports and only creates data inside the supplied test projects.
"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


def request(port, path, method='GET', body=None, raw=None):
    data = raw if raw is not None else (
        json.dumps(body, ensure_ascii=False).encode() if body is not None else None)
    req = urllib.request.Request('http://127.0.0.1:%d%s' % (port, path),
                                 method=method, data=data,
                                 headers={'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req, timeout=5)
    except urllib.error.HTTPError as e:
        response = e
    content = response.read().decode()
    return response.status, dict(response.headers), json.loads(content) if content else None


class Server:
    def __init__(self, project, port, suffix):
        self.project, self.port, self.suffix = project, port, suffix

    def __enter__(self):
        jar = next(p for p in (self.project / 'build/libs').glob('*.jar')
                   if not p.name.endswith('-plain.jar'))
        self.log = (self.project.parent / (self.project.name + self.suffix + '-http.log')).open('w')
        self.process = subprocess.Popen([
            str(Path(os.environ['JAVA_HOME']) / 'bin/java'), '-jar', str(jar),
            '--server.address=127.0.0.1', '--server.port=' + str(self.port)],
            cwd=self.project, stdout=self.log, stderr=subprocess.STDOUT)
        try:
            for _ in range(120):
                if self.process.poll() is not None:
                    raise RuntimeError('Server exited; inspect ' + self.log.name)
                try:
                    if request(self.port, '/products')[0] == 200:
                        return self
                except OSError:
                    pass
                time.sleep(.25)
            raise TimeoutError('Server start timed out')
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def __exit__(self, *args):
        self.process.terminate()
        try:
            self.process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()
        self.log.close()


def check_project(project, day):
    port = 18100 + day
    checks = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    with Server(project, port, '-first'):
        check('fresh list 200 empty', request(port, '/products') == (200, request(port, '/products')[1], []))
        status, headers, first = request(port, '/products', 'POST', {'name': '  노트  ', 'price': 3000})
        check('create 201 trimmed', status == 201 and first['name'] == '노트')
        check('Location actual id', headers['Location'] == '/products/' + str(first['id']))
        one = headers['Location']
        second = request(port, '/products', 'POST', {'name': '펜', 'price': 1000})[2]
        long_name = '가' * 300
        status, _, long_product = request(port, '/products', 'POST', {'name': long_name, 'price': 0})
        check('long name unchanged contract 201', status == 201 and long_product['name'] == long_name)
        status, _, changed = request(port, one, 'PUT', {'name': '  공책  ', 'price': 0})
        check('PUT 200 keeps id and trims', status == 200 and changed == {'id': first['id'], 'name': '공책', 'price': 0})
        check('GET updated values', request(port, one)[2] == changed)
        before = request(port, '/products')[2]
        for label, body in [
            ('blank', {'name': ' ', 'price': 1}),
            ('negative', {'name': '노트', 'price': -1}),
            ('missing price', {'name': '노트'}),
            ('null price', {'name': '노트', 'price': None}),
            ('missing name', {'price': 1}),
            ('null name', {'name': None, 'price': 1}),
            ('string price', {'name': '노트', 'price': 'abc'})]:
            for method, path in [('POST', '/products'), ('PUT', one)]:
                result = request(port, path, method, body)
                check(method + ' ' + label + ' 400', result[0] == 400 and bool(result[2].get('message')))
                check(method + ' ' + label + ' state unchanged', request(port, '/products')[2] == before)
        result = request(port, '/products', 'POST', raw=b'{"name":')
        check('malformed JSON 400', result[0] == 400 and bool(result[2].get('message')))
        missing = '/products/' + str(max(p['id'] for p in before) + 10000)
        check('missing GET 404', request(port, missing)[0] == 404)
        check('missing PUT 404', request(port, missing, 'PUT', {'name': '없음', 'price': 1})[0] == 404)
        check('missing DELETE 404', request(port, missing, 'DELETE')[0] == 404)
        deleted = '/products/' + str(second['id'])
        status, _, content = request(port, deleted, 'DELETE')
        check('DELETE 204 no body', status == 204 and content is None)
        check('repeat DELETE 404', request(port, deleted, 'DELETE')[0] == 404)
        check('deleted GET 404', request(port, deleted)[0] == 404)
        remaining = request(port, '/products')[2]
        check('other products preserved sorted', remaining == sorted([changed, long_product], key=lambda p: p['id']))
    with Server(project, port, '-restart'):
        expected = remaining if day == 19 else []
        check('restart storage behavior', request(port, '/products')[2] == expected)
        if day == 19:
            for item in expected:
                check('delete persisted product', request(port, '/products/' + str(item['id']), 'DELETE')[0] == 204)
    if day == 19:
        with Server(project, port, '-second-restart'):
            check('deletions persisted after second restart', request(port, '/products')[2] == [])
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--projects', type=Path, required=True)
    args = parser.parse_args()
    records = []
    for day in [14, 16, 19]:
        project = args.projects / ('product-api-' + str(day))
        tests = [ET.parse(p).getroot().attrib for p in (project / 'build/test-results/test').glob('TEST-*.xml')]
        assert tests and not any(int(t['failures']) + int(t['errors']) for t in tests)
        checks = check_project(project, day)
        records.append({'day': day, 'tests': tests, 'http_checks': checks})
        print('PASS day', day, 'JUnit', sum(int(t['tests']) for t in tests), 'HTTP/restart checks', len(checks), flush=True)
    p = args.projects / 'order-query-lab/build/test-results/test'
    tests = [ET.parse(f).getroot().attrib for f in p.glob('TEST-*.xml')]
    assert tests and not any(int(t['failures']) + int(t['errors']) for t in tests)
    output = ''.join(ET.parse(f).getroot().findtext('system-out', '') for f in p.glob('TEST-*.xml'))
    assert 'lazy-select-count=4' in output and 'fetch-select-count=1' in output
    records.append({'day': 23, 'tests': tests, 'queries_before': 4, 'queries_after': 1})
    (args.projects / 'evidence.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
    print('PASS order lab: same results, SELECT 4 -> 1', flush=True)

if __name__ == '__main__':
    main()
