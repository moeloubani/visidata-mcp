#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Try to find Python executable
function findPython() {
  const candidates = ['python3', 'python'];
  
  for (const candidate of candidates) {
    try {
      const result = require('child_process').execSync(`${candidate} --version`, { 
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
  
  console.error('❌ Python 3.8+ is required but not found.');
  console.error('Please install Python 3.8 or higher and ensure it\'s in your PATH.');
  process.exit(1);
}

// Check if visidata-mcp Python package is installed
function checkPythonPackage(pythonCmd) {
  try {
    require('child_process').execSync(`${pythonCmd} -c "import visidata_mcp"`, { 
      stdio: 'pipe' 
    });
    return true;
  } catch (e) {
    return false;
  }
}

// Install the Python package
function installPythonPackage(pythonCmd) {
  console.log('📦 Installing visidata-mcp Python package...');
  try {
    require('child_process').execSync(`${pythonCmd} -m pip install visidata-mcp`, { 
      stdio: 'inherit' 
    });
    console.log('✅ Python package installed successfully');
    return true;
  } catch (e) {
    console.error('❌ Failed to install Python package:', e.message);
    return false;
  }
}

// Main execution
function main() {
  const pythonCmd = findPython();
  
  // Check if Python package is installed, install if not
  if (!checkPythonPackage(pythonCmd)) {
    console.log('🔍 visidata-mcp Python package not found, installing...');
    if (!installPythonPackage(pythonCmd)) {
      process.exit(1);
    }
  }
  
  // Run the MCP server
  const args = ['-m', 'visidata_mcp.server', ...process.argv.slice(2)];
  const server = spawn(pythonCmd, args, {
    stdio: 'inherit',
    cwd: process.cwd()
  });
  
  server.on('error', (err) => {
    console.error('❌ Failed to start visidata-mcp server:', err.message);
    process.exit(1);
  });
  
  server.on('exit', (code) => {
    process.exit(code || 0);
  });
  
  // Handle termination signals
  process.on('SIGINT', () => {
    server.kill('SIGINT');
  });
  
  process.on('SIGTERM', () => {
    server.kill('SIGTERM');
  });
}

if (require.main === module) {
  main();
}

module.exports = { main }; 