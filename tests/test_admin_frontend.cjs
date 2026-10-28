// Execute the rendered page script with a minimal DOM to test table behavior.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

class Element {
  constructor() {
    this.children = [];
    this.style = {};
    this.dataset = {};
    this.value = '';
    this.textContent = '';
    this.classList = { add() {}, remove() {} };
    this.listeners = {};
  }
  set innerHTML(value) { this.html = value; this.children = []; }
  get innerHTML() { return this.html || ''; }
  appendChild(child) { this.children.push(child); }
  addEventListener(event, callback) { this.listeners[event] = callback; }
  querySelector(selector) {
    assert.equal(selector, 'b');
    return this.bold ||= new Element();
  }
  getContext() {
    return { clearRect() {}, beginPath() {}, arc() {}, fill() {} };
  }
}

const html = fs.readFileSync(0, 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const elements = new Map();
const get = id => {
  if (!elements.has(id)) elements.set(id, new Element());
  return elements.get(id);
};
const context = {
  document: {
    getElementById: get,
    createElement: () => new Element(),
    querySelectorAll: () => get('categoryNav').children,
  },
  window: { addEventListener() {}, innerWidth: 1024, innerHeight: 768 },
  localStorage: {
    getItem(key) {
      // Stale or malformed browser product data must never be read.
      assert.equal(key, 'cyber_note_v3');
      return null;
    },
    setItem() { assert.fail('Consultation must not write to localStorage'); },
  },
  requestAnimationFrame() {},
  setTimeout() {},
};
vm.createContext(context);
vm.runInContext(script, context);
context.window.onload();
const table = get('mainTable');
const nav = get('categoryNav');
const select = label => {
  const button = nav.children.find(b => b.textContent === label);
  assert.ok(button, `Missing category ${label}`);
  button.listeners.click();
};
const row = id => table.children.find(r => r.dataset.productId === id);

if (process.argv[2] === 'empty') {
  assert.match(table.innerHTML, /Nessun prodotto trovato/);
  assert.deepEqual(nav.children.map(b => b.textContent), ['TUTTI']);
} else {
  assert.equal(table.children.length, 7);
  assert.match(row(1).bold.textContent, /<\/script><img/);
  assert.ok(!row(1).innerHTML.includes('<img'));
  assert.match(row(1).innerHTML, /€2\.50/);
  assert.match(row(1).innerHTML, /€0\.00/);
  assert.match(row(1).innerHTML, /100%/);
  assert.match(row(2).innerHTML, /Esaurito/);
  assert.equal((row(2).innerHTML.match(/—/g) || []).length, 4);
  assert.match(row(3).innerHTML, /50%/);
  assert.match(row(4).innerHTML, /—/);
  assert.ok(!table.children.some(r => r.innerHTML.includes('<button')));
  select('BEVANDE');
  assert.equal(table.children.length, 2);
  select('CIBO');
  assert.deepEqual(table.children.map(r => r.dataset.productId), [4, 3]);
  context.toggleSort();
  assert.deepEqual(table.children.map(r => r.dataset.productId), [3, 4]);
  select('DOLCI');
  assert.equal(table.children[0].dataset.productId, 5);
  select('SENZA CATEGORIA');
  assert.equal(table.children[0].dataset.productId, 6);
  select('STAGIONALI');
  assert.equal(table.children[0].dataset.productId, 7);
  select('TUTTI');
  get('searchInput').value = 'TOAST';
  context.render();
  assert.equal(table.children.length, 1);
  assert.equal(table.children[0].dataset.productId, 3);
  get('searchInput').value = 'inesistente';
  context.render();
  assert.match(table.innerHTML, /Nessun prodotto trovato/);
}
