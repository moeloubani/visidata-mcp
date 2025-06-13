#!/usr/bin/env python3
"""
VisiData MCP Server Setup Verification Script

This script helps verify that your VisiData MCP server installation is correct
and provides specific instructions for fixing common issues.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_check(description, status, details=None):
    """Print a check result."""
    icon = "✅" if status else "❌"
    print(f"{icon} {description}")
    if details:
        for detail in details:
            print(f"   {detail}")


def check_python_version():
    """Check Python version."""
    print_section("Python Version Check")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    is_valid = version.major >= 3 and version.minor >= 8
    
    print_check(
        f"Python Version: {version_str}",
        is_valid,
        [] if is_valid else ["❗ Python 3.8+ required for MCP server"]
    )
    
    # Check which Python we're using
    python_path = sys.executable
    print_check(f"Python Executable: {python_path}", True)
    
    return is_valid


def check_virtual_environment():
    """Check if we're in a virtual environment."""
    print_section("Virtual Environment Check")
    
    venv_path = os.environ.get('VIRTUAL_ENV')
    in_venv = venv_path is not None
    
    print_check(
        "Virtual Environment Active",
        in_venv,
        [f"VIRTUAL_ENV: {venv_path}"] if in_venv else ["❗ Consider using a virtual environment"]
    )
    
    return venv_path


def check_package_installation():
    """Check if required packages are installed."""
    print_section("Package Installation Check")
    
    required_packages = {
        'visidata_mcp': 'VisiData MCP Server',
        'visidata': 'VisiData',
        'mcp': 'MCP Framework',
        'pandas': 'Pandas (data processing)',
        'numpy': 'NumPy (numerical operations)'
    }
    
    all_installed = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            print_check(f"{description}: Installed", True)
        except ImportError:
            print_check(f"{description}: Missing", False)
            all_installed = False
    
    return all_installed


def check_mcp_server_tools():
    """Check if MCP server tools are registered."""
    print_section("MCP Server Tools Check")
    
    try:
        # Try to import and check tools
        from visidata_mcp.server import mcp
        import asyncio
        
        async def count_tools():
            tools = await mcp.list_tools()
            resources = await mcp.list_resources()
            prompts = await mcp.list_prompts()
            return len(tools), len(resources), len(prompts)
        
        tool_count, resource_count, prompt_count = asyncio.run(count_tools())
        
        print_check(f"Tools registered: {tool_count}", tool_count == 8)
        print_check(f"Resources registered: {resource_count}", resource_count == 1)
        print_check(f"Prompts registered: {prompt_count}", prompt_count == 1)
        
        return tool_count == 8
        
    except Exception as e:
        print_check("MCP Server Import", False, [f"Error: {str(e)}"])
        return False


def check_mcp_config():
    """Check MCP configuration files."""
    print_section("MCP Configuration Check")
    
    configs_found = []
    
    # Check for Cursor config
    cursor_config = Path.cwd() / ".cursor" / "mcp.json"
    if cursor_config.exists():
        configs_found.append(("Cursor", cursor_config))
    
    # Check for Claude Desktop config (macOS)
    claude_config = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    if claude_config.exists():
        configs_found.append(("Claude Desktop", claude_config))
    
    if not configs_found:
        print_check("MCP Configuration Files", False, [
            "No MCP configuration files found",
            "Create .cursor/mcp.json for Cursor or Claude Desktop config"
        ])
        return False
    
    config_valid = True
    for name, config_path in configs_found:
        try:
            with open(config_path) as f:
                config = json.load(f)
            
            if 'mcpServers' in config and 'visidata' in config['mcpServers']:
                vd_config = config['mcpServers']['visidata']
                command = vd_config.get('command', '')
                
                # Check if using absolute path
                is_absolute = os.path.isabs(command)
                print_check(
                    f"{name} Config: {config_path}",
                    True,
                    [f"Command: {command}"] + 
                    ([] if is_absolute else ["⚠️  Consider using absolute path to Python"])
                )
            else:
                print_check(f"{name} Config: Missing visidata server", False)
                config_valid = False
                
        except Exception as e:
            print_check(f"{name} Config: Invalid JSON", False, [str(e)])
            config_valid = False
    
    return config_valid


def check_server_startup():
    """Test server startup."""
    print_section("Server Startup Test")
    
    try:
        # Test JSON-RPC initialization
        init_request = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0"}
            }
        })
        
        result = subprocess.run(
            [sys.executable, "-m", "visidata_mcp.server"],
            input=init_request,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 or "protocolVersion" in result.stdout:
            print_check("Server Startup", True, ["Server responds to MCP initialization"])
            return True
        else:
            print_check("Server Startup", False, [
                f"Return code: {result.returncode}",
                f"STDOUT: {result.stdout[:200]}...",
                f"STDERR: {result.stderr[:200]}..."
            ])
            return False
            
    except Exception as e:
        print_check("Server Startup", False, [f"Error: {str(e)}"])
        return False


def provide_recommendations():
    """Provide setup recommendations."""
    print_section("Recommended Next Steps")
    
    print("1. 🔧 Fix any failed checks above")
    print("2. 🚀 Update MCP configuration with absolute Python path:")
    print("   {")
    print('     "mcpServers": {')
    print('       "visidata": {')
    print(f'         "command": "{sys.executable}",')
    print('         "args": ["-m", "visidata_mcp.server"],')
    print(f'         "cwd": "{Path.cwd()}"')
    print('       }')
    print('     }')
    print("   }")
    print("3. 🔄 Restart your MCP client (Cursor/Claude Desktop)")
    print("4. 🎯 Test with a simple query: 'What VisiData tools are available?'")


def main():
    """Run the verification checks."""
    print("🧪 VisiData MCP Server Setup Verification")
    print("This script will help diagnose common setup issues.")
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_environment),
        ("Package Installation", check_package_installation),
        ("MCP Server Tools", check_mcp_server_tools),
        ("MCP Configuration", check_mcp_config),
        ("Server Startup", check_server_startup),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_check(f"{name}: Error", False, [str(e)])
            results.append((name, False))
    
    # Summary
    print_section("Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total} checks")
    
    if passed == total:
        print("🎉 All checks passed! Your VisiData MCP server should be working.")
    else:
        print(f"❌ {total - passed} issues found. See recommendations below.")
        provide_recommendations()


if __name__ == "__main__":
    main() 