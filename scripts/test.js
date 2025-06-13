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
  
  // Test 3: Test MCP server can be imported
  console.log('3. Testing MCP server import...');
  try {
    const result = execSync(`${pythonCmd} -c "from visidata_mcp.server import main; print('✅ Server import successful')"`, { 
      encoding: 'utf8',
      stdio: 'pipe',
      timeout: 5000
    });
    console.log(result.trim());
  } catch (e) {
    console.error('❌ MCP server import failed');
    console.error('Error:', e.message);
    return false;
  }
  
  // Test 4: Test tools registration
  console.log('4. Testing tools registration...');
  try {
    const result = execSync(`${pythonCmd} -c "from visidata_mcp.server import get_supported_formats; print('✅ Tools registration working')"`, { 
      encoding: 'utf8',
      stdio: 'pipe'
    });
    console.log(result.trim());
  } catch (e) {
    console.error('❌ Tools registration failed');
    return false;
  }
  
  console.log('');
  console.log('🎉 All tests passed!');
  console.log('');
  console.log('Your visidata-mcp installation is working correctly!');
  console.log('');
  console.log('Usage in MCP configurations:');
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
  console.log('Note: The MCP server runs as a background service and communicates via stdin/stdout.');
  console.log('');
  
  return true;
}

if (require.main === module) {
  const success = testInstallation();
  process.exit(success ? 0 : 1);
}

module.exports = { testInstallation }; 