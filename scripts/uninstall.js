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
  
  return null;
}

function uninstallPythonPackage() {
  console.log('🗑️  Uninstalling visidata-mcp Python package...');
  
  const pythonCmd = findPython();
  if (!pythonCmd) {
    console.log('Python not found, skipping Python package cleanup');
    return;
  }
  
  try {
    // Check if package is installed
    execSync(`${pythonCmd} -c "import visidata_mcp"`, { stdio: 'pipe' });
    
    // Uninstall the package
    execSync(`${pythonCmd} -m pip uninstall -y visidata-mcp`, { 
      stdio: 'inherit' 
    });
    
    console.log('✅ visidata-mcp Python package uninstalled');
    
  } catch (error) {
    // Package probably wasn't installed, which is fine
    console.log('✅ visidata-mcp Python package was not installed or already removed');
  }
}

if (require.main === module) {
  uninstallPythonPackage();
}

module.exports = { uninstallPythonPackage }; 