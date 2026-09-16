import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {test} from 'node:test';
import vm from 'node:vm';

const fragment = readFileSync(new URL('../assets/native-content-cta.fragment.html', import.meta.url), 'utf8');
const script = fragment.match(/<script>\n([\s\S]*?)\n<\/script>/)?.[1];
assert.ok(script, 'portable fragment has one inline runtime');

function runFragment({itemUrl = 'https://target-board.example/board-path/items/verified-item-path'} = {}) {
  const listeners = new Map();
  const map = new Map();
  const scroller = {scrollTop: 0, scrollHeight: 2000};
  const location = {
    origin: 'https://target-board.example', pathname: '/board-path/', assigned: null,
    assign(value) { this.assigned = value; this.pathname = new URL(value).pathname; }
  };
  const launcher = {dataset: {itemUrl}, disabled: false, textContent: 'Open content item'};
  const root = {
    dataset: {boardUrl: 'https://target-board.example/board-path'},
    querySelectorAll() { return [launcher]; },
    contains(value) { return value === launcher; },
    addEventListener(name, callback) { listeners.set(name, callback); }
  };
  let routeChanged;
  const sessionStorage = {
    setItem(key, value) { map.set(key, value); },
    getItem(key) { return map.has(key) ? map.get(key) : null; },
    removeItem(key) { map.delete(key); }
  };
  const window = {
    location, innerHeight: 700, scrollY: 0,
    addEventListener() {},
    scrollTo(_x, y) { scroller.scrollTop = y; }
  };
  vm.runInNewContext(script, {
    document: {
      querySelector() { return root; }, scrollingElement: scroller, documentElement: scroller,
      body: {}, readyState: 'complete'
    },
    window, location, sessionStorage, URL,
    requestAnimationFrame(callback) { callback(); },
    MutationObserver: class {
      constructor(callback) { routeChanged = callback; }
      observe() {}
    }
  });
  return {listeners, map, scroller, location, launcher, routeChanged};
}

test('same-board item opens natively and route return restores scroll without popstate', () => {
  const page = runFragment();
  page.scroller.scrollTop = 640;
  page.listeners.get('click')({target: {closest() { return page.launcher; }}});
  assert.equal(page.location.assigned, 'https://target-board.example/board-path/items/verified-item-path');
  assert.equal([...page.map.values()][0], '640');
  page.scroller.scrollTop = 0;
  page.routeChanged();
  assert.equal(page.scroller.scrollTop, 0, 'do not restore inside the item route');
  page.location.pathname = '/board-path/';
  page.routeChanged();
  assert.equal(page.scroller.scrollTop, 640);
  assert.equal(page.map.size, 0, 'one-time scroll key is cleared');
});

test('source or cross-board URLs fail closed, and the browser asset has no API secret', () => {
  const page = runFragment({itemUrl: 'https://source.example/article'});
  assert.equal(page.launcher.disabled, true);
  page.listeners.get('click')({target: {closest() { return page.launcher; }}});
  assert.equal(page.location.assigned, null);
  assert.doesNotMatch(fragment, /Authorization|client_secret|api_key|id_[A-Za-z0-9]+/i);
});
