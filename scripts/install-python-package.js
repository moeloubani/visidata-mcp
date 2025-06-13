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
  
  console.error('❌ Python 3.10+ is required but not found');
  process.exit(1);
}

function checkPipx() {
  try {
    execSync('pipx --version', { stdio: 'pipe' });
    return true;
  } catch (e) {
    return false;
  }
}

function installWithPipx() {
  console.log('📦 Installing visidata-mcp with pipx...');
  try {
    execSync('pipx install visidata-mcp', { stdio: 'inherit' });
    
    // Ensure pipx path is set up
    try {
      execSync('pipx ensurepath', { stdio: 'pipe' });
    } catch (e) {
      // Ignore if ensurepath fails
    }
    
    console.log('');
    console.log('🎉 visidata-mcp installed successfully with pipx!');
    console.log('');
    console.log('Note: You may need to restart your terminal or run:');
    console.log('  source ~/.bashrc  # or ~/.zshrc');
    console.log('');
    console.log('You can now use it in your MCP configuration:');
    console.log('  "command": "visidata-mcp"');
    console.log('');
    return true;
  } catch (error) {
    console.log('❌ pipx installation failed');
    return false;
  }
}

function installPythonPackage() {
  console.log('');
  console.log('📦 Installing visidata-mcp Python package...');
  console.log('This may take a few minutes as it installs VisiData and dependencies...');
  
  const pythonCmd = findPython();
  
  try {
    // Try installing normally first
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
    // If the first attempt failed, try with --user flag
    console.log('🔄 System environment protected, trying user installation...');
    
    try {
      execSync(`${pythonCmd} -m pip install --user visidata-mcp`, { 
        stdio: 'inherit' 
      });
      
      // Verify installation
      console.log('✅ Verifying installation...');
      execSync(`${pythonCmd} -c "import visidata_mcp; print('Installation verified')"`, { 
        stdio: 'pipe' 
      });
      
      console.log('');
      console.log('🎉 visidata-mcp installed successfully in user directory!');
      console.log('');
      console.log('You can now use it in your MCP configuration:');
      console.log('  "command": "visidata-mcp"');
      console.log('');
      
    } catch (userError) {
      // If both pip methods failed, try pipx
      console.log('🔄 pip installation failed, trying pipx...');
      
      if (checkPipx()) {
        if (installWithPipx()) {
          return; // Success with pipx
        }
      } else {
        console.log('📦 pipx not found, attempting to install it...');
        try {
          // Try to install pipx with brew (macOS) or suggest manual installation
          if (process.platform === 'darwin') {
            console.log('🍺 Installing pipx with Homebrew...');
            execSync('brew install pipx', { stdio: 'inherit' });
            if (installWithPipx()) {
              return; // Success with pipx after installing it
            }
          }
        } catch (brewError) {
          // Brew failed, continue to error message
        }
      }
      
      console.error('');
      console.error('❌ Failed to install visidata-mcp Python package');
      console.error('');
      console.error('Troubleshooting options:');
      console.error('  1. Use pipx (recommended for applications):');
      console.error('     brew install pipx  # on macOS');
      console.error('     pipx install visidata-mcp');
      console.error('');
      console.error('  2. Use a virtual environment:');
      console.error('     python3 -m venv venv');
      console.error('     source venv/bin/activate');
      console.error('     pip install visidata-mcp');
      console.error('');
      console.error('  3. Use --break-system-packages flag (not recommended):');
      console.error('     python3 -m pip install --break-system-packages visidata-mcp');
      console.error('');
      process.exit(1);
    }
  }
}

if (require.main === module) {
  installPythonPackage();
}

module.exports = { installPythonPackage }; 