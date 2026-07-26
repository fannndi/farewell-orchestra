const fs = require('fs');
const path = require('path');

const files = [
  'opencode.jsonc',
  'profiles/opencode.paid.jsonc',
  'profiles/opencode.hybrid.jsonc',
  'profiles/opencode.free.jsonc'
];

let errors = 0;

for (const file of files) {
  const fullPath = path.join(__dirname, file);
  try {
    const content = fs.readFileSync(fullPath, 'utf8');
    JSON.parse(content);
    console.log(`✅ ${file} — valid JSON`);
    
    const config = JSON.parse(content);
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
  console.log(`\n✅ Semua ${files.length} file valid.`);
} else {
  console.log(`\n❌ ${errors} file error.`);
  process.exit(1);
}
