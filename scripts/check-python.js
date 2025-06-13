#!/usr/bin/env node

const { execSync } = require('child_process');

function checkPython() {
  console.log('🔍 Checking Python requirements...');
  
  const candidates = ['python3', 'python'];
  let pythonCmd = null;
  let pythonVersion = null;
  
  for (const candidate of candidates) {
    try {
      const result = execSync(`${candidate} --version`, { 
        encoding: 'utf8', 
        stdio: 'pipe' 
      });
      
      if (result.includes('Python 3.')) {
        pythonCmd = candidate;
        pythonVersion = result.trim();
        
        // Check if version is 3.10+
        const versionMatch = result.match(/Python 3\.(\d+)/);
        if (versionMatch && parseInt(versionMatch[1]) >= 10) {
          console.log(`✅ Found compatible Python: ${pythonVersion}`);
          return true;
        }
      }
    } catch (e) {
      // Continue to next candidate
    }
  }
  
  if (pythonCmd) {
    console.error(`❌ Found Python (${pythonVersion}) but version 3.10+ is required`);
  } else {
    console.error('❌ Python 3.10+ is required but not found');
  }
  
  console.error('');
  console.error('Please install Python 3.10 or higher:');
  console.error('  macOS: brew install python3');
  console.error('  Ubuntu/Debian: sudo apt install python3 python3-pip');
  console.error('  Windows: Download from https://python.org');
  console.error('');
  
  process.exit(1);
}

if (require.main === module) {
  checkPython();
}

module.exports = { checkPython }; 