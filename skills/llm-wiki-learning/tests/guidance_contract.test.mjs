import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const root = new URL('../', import.meta.url);

async function load(relativePath) {
  return readFile(new URL(relativePath, root), 'utf8');
}

test('core skill requires SVG note previews for embedded Canvas', async () => {
  const skill = await load('SKILL.md');
  assert.match(skill, /\.canvas.*source of truth/i);
  assert.match(skill, /embed only.*\.svg/i);
  assert.match(skill, /canvas_to_svg\.mjs/);
});

test('skill only triggers for explicit Obsidian writeback', async () => {
  const skill = await load('SKILL.md');
  const description = skill.match(/description:\s*["']?([^\n"']+)/)?.[1] ?? '';
  assert.match(description, /explicitly asks/i);
  assert.match(description, /Obsidian/i);
  assert.doesNotMatch(description, /learning or explaining|guide LLM learning/i);
  assert.match(skill, /Do not (?:use|activate|trigger).*chat-only/is);
});

test('Canvas reference requires portrait layout and pure SVG', async () => {
  const rules = await load('references/canvas-diagrams.md');
  assert.match(rules, /top-to-bottom main spine/i);
  assert.match(rules, /height.*greater than.*width/i);
  assert.match(rules, /foreignObject/);
  assert.match(rules, /!\[\[Knowledge\/LLM\/Canvas\/<name>\.svg\]\]/);
});

test('note template requires selective orientation sentences and visual budget', async () => {
  const template = await load('references/note-templates.md');
  assert.match(template, /one-sentence orientation/i);
  assert.match(template, /one summary callout/i);
  assert.match(template, /zero or one embedded SVG/i);
  assert.match(template, /information hierarchy/i);
});
