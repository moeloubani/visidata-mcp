#!/usr/bin/env python3
"""
VisiData MCP Setup Helper

This script helps users set up VisiData MCP by:
1. Installing the npm package
2. Configuring it for their AI application (Cursor, Windsurf, Claude Desktop)

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

def check_npm():
    """Check if npm is available."""
    print("📦 Checking for npm...")
    success, output, _ = run_command("npm --version")
    if success:
        print(f"✅ npm found: {output}")
        return True
    else:
        print("❌ npm not found")
        print("Please install Node.js from https://nodejs.org")
        return False

def install_visidata_mcp():
    """Install visidata-mcp with npm."""
    print("\n📦 Installing visidata-mcp...")
    print("Running: npm install -g @moeloubani/visidata-mcp")
    
    success, stdout, stderr = run_command("npm install -g @moeloubani/visidata-mcp", capture_output=False)
    
    if success:
        print("✅ visidata-mcp installed successfully!")
        return True
    else:
        print("❌ Installation failed")
        if "permission" in stderr.lower():
            print("💡 Try with sudo: sudo npm install -g @moeloubani/visidata-mcp")
        print(f"Error: {stderr}")
        return False

def verify_installation():
    """Verify that visidata-mcp command is available."""
    print("\n🔍 Verifying installation...")
    success, output, _ = run_command("visidata-mcp --version")
    if success:
        print("✅ visidata-mcp command is working!")
        return True
    else:
        print("❌ visidata-mcp command not found")
        print("💡 Try reinstalling or check if npm global bin is in your PATH")
        return False

def configure_cursor():
    """Configure Cursor AI."""
    print("\n📝 Configuring Cursor AI...")
    
    config = {
        "mcpServers": {
            "visidata": {
                "command": "visidata-mcp"
            }
        }
    }
    
    cursor_dir = Path(".cursor")
    cursor_dir.mkdir(exist_ok=True)
    
    config_file = cursor_dir / "mcp.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Created {config_file}")
    print("📄 Configuration:")
    print(json.dumps(config, indent=2))
    return config_file

def configure_windsurf():
    """Configure Windsurf."""
    print("\n📝 Configuring Windsurf...")
    
    config = {
        "mcpServers": {
            "visidata": {
                "command": "visidata-mcp"
            }
        }
    }
    
    windsurf_dir = Path(".windsurf")
    windsurf_dir.mkdir(exist_ok=True)
    
    config_file = windsurf_dir / "mcp.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Created {config_file}")
    print("📄 Configuration:")
    print(json.dumps(config, indent=2))
    return config_file

def configure_claude_desktop():
    """Show Claude Desktop configuration."""
    print("\n📝 Claude Desktop configuration:")
    
    config = {
        "mcpServers": {
            "visidata": {
                "command": "visidata-mcp"
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

def main():
    """Main setup process."""
    print("🚀 VisiData MCP Setup Helper")
    print("=" * 40)
    print("This will help you set up VisiData MCP with your AI application")
    print("")
    
    # Step 1: Check npm
    if not check_npm():
        return 1
    
    # Step 2: Install visidata-mcp
    print("\n📋 Step 1: Install VisiData MCP")
    if not install_visidata_mcp():
        return 1
    
    # Step 3: Verify installation
    if not verify_installation():
        print("⚠️  Installation may have issues, but continuing...")
    
    # Step 4: Configure AI application
    print("\n📋 Step 2: Configure Your AI Application")
    print("Which AI application are you using?")
    print("1. Cursor AI")
    print("2. Windsurf")
    print("3. Claude Desktop")
    print("4. Skip configuration")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        configure_cursor()
        app_name = "Cursor"
    elif choice == "2":
        configure_windsurf()
        app_name = "Windsurf"
    elif choice == "3":
        configure_claude_desktop()
        app_name = "Claude Desktop"
    elif choice == "4":
        print("⏭️  Skipping configuration")
        app_name = "your AI application"
    else:
        print("❌ Invalid choice")
        return 1
    
    # Final instructions
    print("\n🎉 Setup Complete!")
    print("=" * 40)
    print("Next steps:")
    print(f"1. ✅ Restart {app_name} completely")
    print("2. ✅ Look for 'Available MCP Tools' or similar in the chat")
    print("3. ✅ Try: 'Please analyze this CSV file: /path/to/file.csv'")
    print("")
    print("Available tools: load_data, analyze_data, convert_data, filter_data, sort_data, etc.")
    print("")
    print("🔧 Troubleshooting:")
    print("- If you see '0 tools available', restart your AI app completely")
    print("- Make sure the config file was created in the right location")
    print("- Check that 'visidata-mcp --version' works in terminal")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
        sys.exit(1) 