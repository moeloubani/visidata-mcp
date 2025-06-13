#!/usr/bin/env node

const { execSync, spawn } = require('child_process');

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

function testInstallation() {
  console.log('🧪 Testing visidata-mcp installation...');
  console.log('');
  
  // Test 1: Check Python
  console.log('1. Checking Python installation...');
  const pythonCmd = findPython();
  if (!pythonCmd) {
    console.error('❌ Python not found');
    return false;
  }
  console.log(`✅ Python found: ${pythonCmd}`);
  
  // Test 2: Check Python package
  console.log('2. Checking visidata-mcp Python package...');
  try {
    execSync(`${pythonCmd} -c "import visidata_mcp"`, { stdio: 'pipe' });
    console.log('✅ visidata-mcp Python package installed');
  } catch (e) {
    console.error('❌ visidata-mcp Python package not found');
    return false;
  }
  
  // Test 3: Test MCP server startup
  console.log('3. Testing MCP server startup...');
  try {
    const result = execSync(`${pythonCmd} -m visidata_mcp.server --help`, { 
      encoding: 'utf8',
      stdio: 'pipe',
      timeout: 10000
    });
    console.log('✅ MCP server can start');
  } catch (e) {
    console.error('❌ MCP server failed to start');
    console.error('Error:', e.message);
    return false;
  }
  
  // Test 4: Test tools registration
  console.log('4. Testing tools registration...');
  try {
    const result = execSync(`${pythonCmd} -c "from visidata_mcp.server import get_supported_formats; print('Tools available')"`, { 
      encoding: 'utf8',
      stdio: 'pipe'
    });
    console.log('✅ Tools registration working');
  } catch (e) {
    console.error('❌ Tools registration failed');
    return false;
  }
  
  console.log('');
  console.log('🎉 All tests passed!');
  console.log('');
  console.log('You can now use visidata-mcp in your MCP configuration:');
  console.log('');
  console.log('Claude Desktop (claude_desktop_config.json):');
  console.log(JSON.stringify({
    mcpServers: {
      visidata: {
        command: "visidata-mcp"
      }
    }
  }, null, 2));
  console.log('');
  console.log('Cursor (.cursor/mcp.json):');
  console.log(JSON.stringify({
    mcpServers: {
      visidata: {
        command: "visidata-mcp"
      }
    }
  }, null, 2));
  console.log('');
  
  return true;
}

if (require.main === module) {
  const success = testInstallation();
  process.exit(success ? 0 : 1);
}

module.exports = { testInstallation }; 