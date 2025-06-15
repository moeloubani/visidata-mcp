#!/usr/bin/env python3
"""
VisiData MCP Setup Helper

This script helps users set up VisiData MCP by:
1. Checking their system
2. Recommending installation method
3. Generating configuration files
4. Testing the installation

Run this script and follow the prompts!
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path

def run_command(cmd, capture_output=True):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_python():
    """Check Python version."""
    print("🐍 Checking Python version...")
    success, output, _ = run_command("python3 --version")
    if not success:
        print("❌ Python 3 not found")
        return False, None
    
    version_str = output.replace("Python ", "")
    version_parts = version_str.split(".")
    major, minor = int(version_parts[0]), int(version_parts[1])
    
    if major < 3 or (major == 3 and minor < 10):
        print(f"❌ Python {version_str} found, but 3.10+ is required")
        return False, version_str
    
    print(f"✅ Python {version_str} (compatible)")
    return True, version_str

def check_pipx():
    """Check if pipx is available."""
    print("📦 Checking for pipx...")
    success, output, _ = run_command("pipx --version")
    if success:
        print(f"✅ pipx found: {output}")
        return True
    else:
        print("❌ pipx not found")
        return False

def check_npm():
    """Check if npm is available."""
    print("📦 Checking for npm...")
    success, output, _ = run_command("npm --version")
    if success:
        print(f"✅ npm found: {output}")
        return True
    else:
        print("❌ npm not found")
        return False

def install_pipx():
    """Guide user through pipx installation."""
    print("\n🔧 Installing pipx...")
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("Detected macOS. Trying to install pipx with Homebrew...")
        success, _, _ = run_command("brew install pipx", capture_output=False)
        if success:
            print("✅ pipx installed with Homebrew")
            return True
    
    print("Trying to install pipx with pip...")
    success, _, _ = run_command("python3 -m pip install --user pipx", capture_output=False)
    if success:
        print("✅ pipx installed with pip")
        # Add to PATH
        run_command("python3 -m pipx ensurepath", capture_output=False)
        return True
    
    print("❌ Failed to install pipx automatically")
    print("Please install pipx manually:")
    print("  macOS: brew install pipx")
    print("  Linux: python3 -m pip install --user pipx")
    return False

def install_visidata_mcp():
    """Install visidata-mcp with pipx."""
    print("\n📦 Installing visidata-mcp...")
    success, stdout, stderr = run_command("pipx install visidata-mcp", capture_output=True)
    
    # Check if it's already installed
    if not success and "already seems to be installed" in stderr:
        print("✅ visidata-mcp already installed!")
        return True
    elif success:
        print("✅ visidata-mcp installed successfully!")
        return True
    else:
        print("❌ Installation failed")
        print(f"Error: {stderr}")
        return False

def find_visidata_command():
    """Find the visidata-mcp command path."""
    print("\n🔍 Finding visidata-mcp command...")
    
    # Check pipx installation
    pipx_path = Path.home() / ".local" / "bin" / "visidata-mcp"
    if pipx_path.exists():
        print(f"✅ Found pipx version: {pipx_path}")
        return str(pipx_path)
    
    # Check which command finds it
    success, output, _ = run_command("which visidata-mcp")
    if success:
        print(f"✅ Found in PATH: {output}")
        # Check if it's npm version
        if "nvm" in output or "node" in output:
            print("⚠️  This appears to be the npm version")
            print("⚠️  npm version may have issues with externally managed Python")
            if pipx_path.exists():
                print(f"⚠️  Recommend using pipx version: {pipx_path}")
                return str(pipx_path)
        return output
    
    print("❌ visidata-mcp command not found")
    return None

def generate_cursor_config(command_path):
    """Generate Cursor configuration."""
    print("\n📝 Generating Cursor configuration...")
    
    config = {
        "mcpServers": {
            "visidata": {
                "command": command_path
            }
        }
    }
    
    cursor_dir = Path(".cursor")
    cursor_dir.mkdir(exist_ok=True)
    
    config_file = cursor_dir / "mcp.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Created {config_file}")
    print("📄 Configuration content:")
    print(json.dumps(config, indent=2))
    return config_file

def generate_claude_config(command_path):
    """Generate Claude Desktop configuration."""
    print("\n📝 Claude Desktop configuration:")
    
    config = {
        "mcpServers": {
            "visidata": {
                "command": command_path
            }
        }
    }
    
    system = platform.system()
    if system == "Darwin":  # macOS
        config_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:  # Windows
        config_path = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    
    print(f"📍 Config file location: {config_path}")
    print("📄 Add this to your Claude Desktop configuration:")
    print(json.dumps(config, indent=2))
    
    return config_path

def test_installation(command_path):
    """Test the installation with MCP Inspector."""
    print("\n🧪 Testing installation...")
    print("Starting MCP Inspector...")
    print("This will open a browser window for testing.")
    print("Press Ctrl+C to stop the test when done.")
    
    try:
        cmd = f"npx @modelcontextprotocol/inspector {command_path}"
        print(f"Running: {cmd}")
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print("\n✅ Test stopped by user")
    except Exception as e:
        print(f"❌ Test failed: {e}")

def main():
    """Main setup process."""
    print("🚀 VisiData MCP Setup Helper")
    print("=" * 40)
    
    # Step 1: Check Python
    python_ok, python_version = check_python()
    if not python_ok:
        print("\n❌ Python 3.10+ is required. Please install Python and try again.")
        return 1
    
    # Step 2: Check pipx (preferred) or npm
    has_pipx = check_pipx()
    has_npm = check_npm()
    
    if not has_pipx and not has_npm:
        print("\n❌ Neither pipx nor npm found")
        print("Installing pipx (recommended)...")
        if not install_pipx():
            return 1
        has_pipx = True
    
    # Step 3: Install visidata-mcp
    if has_pipx:
        print("\n✅ Using pipx installation (recommended)")
        if not install_visidata_mcp():
            return 1
    else:
        print("\n⚠️  Only npm available")
        print("You can install with: npm install -g @moeloubani/visidata-mcp@beta")
        print("Note: npm version may have issues with externally managed Python")
        return 1
    
    # Step 4: Find command
    command_path = find_visidata_command()
    if not command_path:
        print("\n❌ Could not find visidata-mcp command after installation")
        return 1
    
    # Step 5: Generate configurations
    print("\n📋 Configuration Options:")
    print("1. Cursor AI (current directory)")
    print("2. Claude Desktop")
    print("3. Both")
    
    choice = input("\nWhat would you like to configure? (1/2/3): ").strip()
    
    if choice in ["1", "3"]:
        generate_cursor_config(command_path)
    
    if choice in ["2", "3"]:
        generate_claude_config(command_path)
    
    # Step 6: Test
    print("\n🧪 Would you like to test the installation? (y/n): ", end="")
    if input().strip().lower() == "y":
        test_installation(command_path)
    
    # Final instructions
    print("\n🎉 Setup Complete!")
    print("=" * 40)
    print("Next steps:")
    print("1. ✅ Restart your AI application (Cursor/Claude Desktop)")
    print("2. ✅ Look for 'Available MCP Tools' in the chat")
    print("3. ✅ Try: 'Please analyze this CSV file: /path/to/file.csv'")
    print("\nTools available: load_data, analyze_data, convert_data, filter_data, sort_data, etc.")
    
    if choice == "1":
        print(f"\n📁 Cursor config created in: {Path('.cursor/mcp.json').absolute()}")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
        sys.exit(1) 