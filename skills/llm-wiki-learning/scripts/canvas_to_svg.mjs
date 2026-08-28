#!/usr/bin/env node
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const PADDING = 36;
const CHAR_WIDTH = 8;
const LINE_HEIGHT = 22;
const COLORS = {
  '1': ['#f2c6cb', '#dc5b67'],
  '2': ['#bce3d9', '#18a87d'],
  '3': ['#efd77e', '#dfa900'],
  '4': ['#f1b775', '#e17400'],
  '5': ['#d7c8ee', '#7653d6'],
  '6': ['#8edbd8', '#00a7a2'],
  default: ['#eee8dc', '#8f887d']
};

function escapeXml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;');
}

function parseMarkdown(line) {
  const trimmed = line.trim();
  const heading = /^#{1,6}\s+/.test(trimmed) || /^\*\*[^*]+\*\*$/.test(trimmed);
  const text = trimmed
    .replace(/^#{1,6}\s+/, '')
    .replace(/^[-*]\s+/, '• ')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/`([^`]+)`/g, '$1')
    .trim();
  return { text, heading };
}

function wrapText(text, maxChars) {
  const chars = Array.from(text);
  if (chars.length <= maxChars) return [text];
  if (!/\s/.test(text)) {
    const lines = [];
    while (chars.length) lines.push(chars.splice(0, maxChars).join(''));
    return lines;
  }
  const words = text.split(/\s+/);
  const lines = [];
  let current = '';
  for (const word of words) {
    if (Array.from(word).length > maxChars) {
      if (current) lines.push(current);
      const longWord = Array.from(word);
      while (longWord.length > maxChars) lines.push(longWord.splice(0, maxChars).join(''));
      current = longWord.join('');
      continue;
    }
    const candidate = current ? `${current} ${word}` : word;
    if (Array.from(candidate).length <= maxChars) current = candidate;
    else {
      lines.push(current);
      current = word;
    }
  }
  if (current) lines.push(current);
  return lines;
}

function nodeLines(node) {
  const maxChars = Math.max(12, Math.floor((node.width - 40) / CHAR_WIDTH));
  return String(node.text ?? node.file ?? node.url ?? node.id)
    .split('\n')
    .flatMap(line => {
      const parsed = parseMarkdown(line);
      return wrapText(parsed.text, maxChars).map(text => ({ ...parsed, text }));
    });
}

function anchor(node, side) {
  if (side === 'top') return [node.x + node.width / 2, node.y];
  if (side === 'left') return [node.x, node.y + node.height / 2];
  if (side === 'right') return [node.x + node.width, node.y + node.height / 2];
  return [node.x + node.width / 2, node.y + node.height];
}

function edgePath(edge, byId, offsetX, offsetY) {
  const from = byId.get(edge.fromNode);
  const to = byId.get(edge.toNode);
  if (!from || !to) return '';
  const [x1, y1] = anchor(from, edge.fromSide);
  const [x2, y2] = anchor(to, edge.toSide);
  const bend = Math.max(40, Math.abs(y2 - y1) / 2);
  return `<path d="M ${x1 + offsetX} ${y1 + offsetY} C ${x1 + offsetX} ${y1 + offsetY + bend}, ${x2 + offsetX} ${y2 + offsetY - bend}, ${x2 + offsetX} ${y2 + offsetY}" marker-end="url(#arrow)"/>`;
}

function renderNode(node, offsetX, offsetY) {
  const [fill, stroke] = COLORS[node.color] ?? COLORS.default;
  const x = node.x + offsetX;
  const y = node.y + offsetY;
  const lines = nodeLines(node);
  const startY = y + Math.max(32, (node.height - (lines.length - 1) * LINE_HEIGHT) / 2);
  const tspans = lines
    .map((line, index) => {
      const size = line.heading ? ' font-size="17"' : '';
      return `<tspan x="${x + 20}" y="${startY + index * LINE_HEIGHT}"${size}>${escapeXml(line.text)}</tspan>`;
    })
    .join('');
  return `<g data-node-id="${escapeXml(node.id)}"><rect x="${x}" y="${y}" width="${node.width}" height="${node.height}" rx="14" fill="${fill}" stroke="${stroke}"/><text>${tspans}</text></g>`;
}

export function convertCanvasJson(jsonText) {
  let canvas;
  try {
    canvas = JSON.parse(jsonText);
  } catch (error) {
    throw new Error(`Invalid Canvas JSON: ${error.message}`);
  }
  if (!Array.isArray(canvas.nodes)) throw new Error('Canvas nodes must be an array');
  if (!canvas.nodes.length) throw new Error('Canvas must contain at least one node');
  const edges = Array.isArray(canvas.edges) ? canvas.edges : [];
  const minX = Math.min(...canvas.nodes.map(node => node.x));
  const minY = Math.min(...canvas.nodes.map(node => node.y));
  const maxX = Math.max(...canvas.nodes.map(node => node.x + node.width));
  const maxY = Math.max(...canvas.nodes.map(node => node.y + node.height));
  const width = maxX - minX + PADDING * 2;
  const height = maxY - minY + PADDING * 2;
  const offsetX = PADDING - minX;
  const offsetY = PADDING - minY;
  const warnings = width >= height
    ? [`Canvas is not portrait-oriented: width=${width}, height=${height}`]
    : [];
  const byId = new Map(canvas.nodes.map(node => [node.id, node]));
  const renderedEdges = edges
    .map(edge => edgePath(edge, byId, offsetX, offsetY))
    .filter(Boolean)
    .join('');
  const renderedNodes = canvas.nodes
    .map(node => renderNode(node, offsetX, offsetY))
    .join('');
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" role="img">` +
    `<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#9a958b"/></marker></defs>` +
    `<rect width="${width}" height="${height}" rx="18" fill="#f7f3e9"/>` +
    `<g id="edges"><g fill="none" stroke="#9a958b" stroke-width="4" stroke-linecap="round">${renderedEdges}</g></g>` +
    `<g id="nodes"><g font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="15" fill="#26231f" stroke-width="3">${renderedNodes}</g></g>` +
    `</svg>\n`;
  return { svg, warnings };
}

async function main() {
  const [input, output] = process.argv.slice(2);
  if (!input || !output) throw new Error('Usage: canvas_to_svg.mjs input.canvas output.svg');
  const { svg, warnings } = convertCanvasJson(await readFile(input, 'utf8'));
  await writeFile(output, svg);
  for (const warning of warnings) console.error(`Warning: ${warning}`);
}

const isCli = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isCli) {
  main().catch(error => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
