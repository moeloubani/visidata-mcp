#!/usr/bin/env node

const { execSync } = require('child_process');

function findPython() {
  const candidates = ['python3', 'python'];
  
  for (const candidate of candidates) {
    try {
      const result = execSync(`${candidate} --version`, { 
        encoding: 'utf8', 
        stdio: 'pipe' 
      });
      if (result.includes('Python 3.')) {
        return candidate;
      }
    } catch (e) {
      // Continue to next candidate
    }
  }
  
  console.error('❌ Python 3.8+ is required but not found');
  process.exit(1);
}

function installPythonPackage() {
  console.log('');
  console.log('📦 Installing visidata-mcp Python package...');
  console.log('This may take a few minutes as it installs VisiData and dependencies...');
  
  const pythonCmd = findPython();
  
  try {
    // First upgrade pip to avoid issues
    console.log('🔄 Upgrading pip...');
    execSync(`${pythonCmd} -m pip install --upgrade pip`, { 
      stdio: 'pipe' 
    });
    
    // Install the package
    console.log('📦 Installing visidata-mcp...');
    execSync(`${pythonCmd} -m pip install visidata-mcp`, { 
      stdio: 'inherit' 
    });
    
    // Verify installation
    console.log('✅ Verifying installation...');
    execSync(`${pythonCmd} -c "import visidata_mcp; print('Installation verified')"`, { 
      stdio: 'pipe' 
    });
    
    console.log('');
    console.log('🎉 visidata-mcp installed successfully!');
    console.log('');
    console.log('You can now use it in your MCP configuration:');
    console.log('  "command": "visidata-mcp"');
    console.log('');
    
  } catch (error) {
    console.error('');
    console.error('❌ Failed to install visidata-mcp Python package');
    console.error('Error:', error.message);
    console.error('');
    console.error('You may need to:');
    console.error('  1. Ensure pip is installed: python3 -m pip --version');
    console.error('  2. Try with --user flag: python3 -m pip install --user visidata-mcp');
    console.error('  3. Use a virtual environment');
    console.error('');
    process.exit(1);
  }
}

if (require.main === module) {
  installPythonPackage();
}

module.exports = { installPythonPackage }; 