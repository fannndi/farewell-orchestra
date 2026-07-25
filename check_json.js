const fs = require('fs');
const content = fs.readFileSync('opencode.paid.jsonc', 'utf8');

const lines = content.split('\n');
const stripped = lines.map(line => {
  let inString = false;
  let escaped = false;
  for (let i = 0; i < line.length - 1; i++) {
    const c = line[i];
    if (escaped) { escaped = false; continue; }
    if (c === '\\') { escaped = true; continue; }
    if (c === '"' && !escaped) { inString = !inString; continue; }
    if (c === '/' && line[i+1] === '/' && !inString) {
      return line.substring(0, i);
    }
  }
  return line;
}).join('\n');

const json = stripped.replace(/\/\*[\s\S]*?\*\//g, '');

try {
  JSON.parse(json);
  console.log('VALID JSON');
} catch(e) {
  console.log('INVALID JSON:', e.message);
  console.log('Error at position:', e.message.match(/position (\d+)/)?.[1]);
  const pos = parseInt(e.message.match(/position (\d+)/)?.[1] || '0');
  console.log('Context:', JSON.stringify(json.substring(Math.max(0, pos-20), pos+20)));
}