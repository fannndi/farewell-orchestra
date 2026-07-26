// Validasi SEMUA profile JSON files
const fs = require('fs');
const path = require('path');

const profiles = [
  'profiles/opencode.paid.jsonc',
  'profiles/opencode.hybrid.jsonc',
  'profiles/opencode.free.jsonc'
];

function stripJsoncComments(content) {
  const lines = content.split('\n');
  const stripped = lines.map(line => {
    let inString = false;
    let escaped = false;
    for (let i = 0; i < line.length; i++) {
      const c = line[i];
      if (escaped) { escaped = false; continue; }
      if (c === '\\') { escaped = true; continue; }
      if (c === '"' && !escaped) { inString = !inString; continue; }
      if (c === '/' && line[i + 1] === '/' && !inString) {
        return line.substring(0, i);
      }
    }
    return line;
  }).join('\n');
  // Strip /* block */ comments
  return stripped.replace(/\/\*[\s\S]*?\*\//g, '');
}

let errors = 0;

for (const file of profiles) {
  const fullPath = path.join(__dirname, file);
  try {
    let content = fs.readFileSync(fullPath, 'utf8');
    content = stripJsoncComments(content);
    const config = JSON.parse(content);
    console.log(`✅ ${file} — valid JSON`);
    
    const agents = Object.keys(config.agent || {}).filter(a => 
      ['orchestrator', 'researcher', 'reviewer', 'executor'].includes(a)
    );
    if (agents.length < 4) {
      console.log(`   ⚠️  Hanya ${agents.length}/4 agent utama ditemukan`);
    }
  } catch (e) {
    console.log(`❌ ${file} — ${e.message}`);
    errors++;
  }
}

if (errors === 0) {
  console.log(`\n✅ Semua ${profiles.length} profile valid.`);
} else {
  console.log(`\n❌ ${errors} profile error.`);
  process.exit(1);
}
