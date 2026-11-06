'use strict';

function renderItems(items) {
  if (items.length === 0) return '(empty)';
  return items.map((item) => `[${item.done ? 'x' : ' '}] ${item.title}`).join('\n');
}

function renderCount(items) {
  const done = items.filter((item) => item.done).length;
  return `${done}/${items.length} done`;
}

module.exports = { renderItems, renderCount };
