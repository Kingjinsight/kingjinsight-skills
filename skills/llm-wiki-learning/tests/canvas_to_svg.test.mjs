import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

import { convertCanvasJson } from '../scripts/canvas_to_svg.mjs';

const fixture = JSON.stringify({
  nodes: [
    { id: 'a', type: 'text', text: '## Input\n- cat & dog', x: 0, y: 0, width: 280, height: 120, color: '1' },
    { id: 'b', type: 'text', text: '**Output**\nsemantic <vector>', x: 0, y: 220, width: 280, height: 120, color: '2' }
  ],
  edges: [
    { id: 'e1', fromNode: 'a', fromSide: 'bottom', toNode: 'b', toSide: 'top' }
  ]
});

test('renders text nodes and edges as pure SVG', () => {
  const { svg, warnings } = convertCanvasJson(fixture);
  assert.match(svg, /^<svg[\s\S]*<g id="edges">[\s\S]*<g id="nodes">/);
  assert.match(svg, /Input/);
  assert.match(svg, /cat &amp; dog/);
  assert.match(svg, /semantic &lt;vector&gt;/);
  assert.match(svg, /marker-end="url\(#arrow\)"/);
  assert.doesNotMatch(svg, /foreignObject|<script|(?:href|src)="https?:\/\//);
  assert.deepEqual(warnings, []);
});

test('uses portrait viewBox for portrait Canvas', () => {
  const { svg } = convertCanvasJson(fixture);
  const [, width, height] = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  assert.ok(Number(height) > Number(width));
});

test('wraps Latin text at word boundaries', () => {
  const canvas = JSON.stringify({
    nodes: [
      { id: 'a', type: 'text', text: '- Intrinsic: similarity / analogy', x: 0, y: 0, width: 280, height: 120 }
    ],
    edges: []
  });
  const { svg } = convertCanvasJson(canvas);
  assert.match(svg, />• Intrinsic: similarity \/<\/tspan><tspan[^>]*>analogy<\/tspan>/);
  assert.doesNotMatch(svg, />anal<\/tspan><tspan[^>]*>ogy<\/tspan>/);
});

test('renders Markdown headings with visual hierarchy', () => {
  const { svg } = convertCanvasJson(fixture);
  assert.match(svg, /<tspan[^>]*font-size="17"[^>]*>Input<\/tspan>/);
  assert.doesNotMatch(svg, /font-weight=/);
});

test('warns when source Canvas is not portrait-oriented', () => {
  const wide = JSON.stringify({
    nodes: [
      { id: 'a', type: 'text', text: 'A', x: 0, y: 0, width: 280, height: 120 },
      { id: 'b', type: 'text', text: 'B', x: 500, y: 0, width: 280, height: 120 }
    ],
    edges: []
  });
  const { warnings } = convertCanvasJson(wide);
  assert.match(warnings[0], /not portrait-oriented/);
});

test('rejects malformed Canvas JSON', () => {
  assert.throws(() => convertCanvasJson('{bad json'), /Invalid Canvas JSON/);
  assert.throws(() => convertCanvasJson('{}'), /nodes must be an array/);
});

test('CLI writes SVG and reports orientation warnings', async () => {
  const dir = await mkdtemp(path.join(tmpdir(), 'canvas-svg-'));
  const input = path.join(dir, 'wide.canvas');
  const output = path.join(dir, 'wide.svg');
  const wide = JSON.stringify({
    nodes: [
      { id: 'a', type: 'text', text: 'A', x: 0, y: 0, width: 280, height: 120 },
      { id: 'b', type: 'text', text: 'B', x: 500, y: 0, width: 280, height: 120 }
    ],
    edges: []
  });
  await writeFile(input, wide);
  const script = fileURLToPath(new URL('../scripts/canvas_to_svg.mjs', import.meta.url));
  const result = spawnSync(process.execPath, [script, input, output], { encoding: 'utf8' });
  assert.ifError(result.error);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stderr, /not portrait-oriented/);
  assert.match(await readFile(output, 'utf8'), /^<svg/);
});
