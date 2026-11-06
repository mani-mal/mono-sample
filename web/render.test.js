'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const render = require('./render.js');

test('renderItems empty', () => {
  assert.equal(render.renderItems([]), '(empty)');
});

test('renderItems mixed', () => {
  const out = render.renderItems([
    { title: 'one', done: false },
    { title: 'two', done: true },
  ]);
  assert.match(out, /\[ \] one/);
  assert.match(out, /\[x\] two/);
});

test('renderCount', () => {
  assert.equal(render.renderCount([{ done: true }, { done: false }, { done: true }]), '2/3 done');
});
