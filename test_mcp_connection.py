#!/usr/bin/env python3
"""
Test script to verify VisiData MCP server configuration for Cursor
"""

import json
import os
import subprocess
import sys
from pathlib import Path
import asyncio

def test_cursor_mcp_config():
    """Test that the Cursor MCP configuration is properly set up."""
    
    print("🧪 Testing VisiData MCP Server Configuration for Cursor...")
    print("=" * 60)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check if virtual environment is active
    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        print(f"🐍 Virtual environment: {venv_path}")
    else:
        print("⚠️  No virtual environment detected")
    
    # Check if the package is installed
    try:
        import visidata_mcp
        print(f"✅ visidata_mcp package found: {visidata_mcp.__file__}")
    except ImportError:
        print("❌ visidata_mcp package not found - run 'pip install -e .' first")
        return False
    
    # Check if .cursor directory exists
    cursor_dir = current_dir / ".cursor"
    if not cursor_dir.exists():
        print(f"📁 Creating .cursor directory: {cursor_dir}")
        cursor_dir.mkdir(exist_ok=True)
    
    # Check MCP configuration file
    mcp_config_file = cursor_dir / "mcp.json"
    if mcp_config_file.exists():
        print(f"📄 MCP config file found: {mcp_config_file}")
        
        # Validate JSON
        try:
            with open(mcp_config_file, 'r') as f:
                config = json.load(f)
            print("✅ MCP configuration is valid JSON")
            print(f"🔧 Configured servers: {list(config.get('mcpServers', {}).keys())}")
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in MCP config: {e}")
            return False
    else:
        print(f"❌ MCP config file not found: {mcp_config_file}")
        return False
    
    # Test importing server functions
    try:
        from visidata_mcp.server import (
            load_data, get_data_sample, analyze_data, 
            get_supported_formats, filter_data, get_column_stats
        )
        print("✅ All MCP server functions imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import server functions: {e}")
        return False
    
    # Test a simple function
    try:
        result = get_supported_formats()
        formats = json.loads(result)
        print(f"✅ get_supported_formats() works - {formats['total_formats']} formats supported")
    except Exception as e:
        print(f"❌ Error testing get_supported_formats(): {e}")
        return False
    
    print("\n🎉 All tests passed!")
    print("\n📋 Next steps:")
    print("1. Restart Cursor")
    print("2. Open a new chat in Cursor")
    print("3. Look for 'Available MCP Tools' indicator")
    print("4. Try asking: 'What VisiData tools are available?'")
    
    return True

async def test_mcp_stdio():
    """Test MCP server via stdio transport."""
    print("Testing MCP server via stdio...")
    
    # Path to the virtual environment's Python
    venv_python = Path("/Users/moe/Dev/visidata-mcp/venv/bin/python")
    if not venv_python.exists():
        print(f"Error: Virtual environment Python not found at {venv_python}")
        return False
    
    try:
        # Start the MCP server process
        process = subprocess.Popen(
            [str(venv_python), "-m", "visidata_mcp.server"],
            cwd="/Users/moe/Dev/visidata-mcp",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send initialization request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("Sending initialization request...")
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Wait a bit for response
        await asyncio.sleep(2)
        
        # Try to read response
        try:
            # Check if process is still running
            if process.poll() is None:
                print("✓ Server process is running")
                
                # Try to get some output
                process.stdin.write('{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}\n')
                process.stdin.flush()
                
                await asyncio.sleep(1)
                
                # Terminate process
                process.terminate()
                stdout, stderr = process.communicate(timeout=5)
                
                print(f"✓ Server started successfully")
                if stdout:
                    print(f"STDOUT: {stdout[:500]}...")
                if stderr:
                    print(f"STDERR: {stderr[:500]}...")
                    
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"✗ Server process exited with code {process.returncode}")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            print(f"✗ Server process timed out")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error testing MCP server: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_cursor_mcp_config()
    if not success:
        sys.exit(1)
    
    result = asyncio.run(test_mcp_stdio())
    sys.exit(0 if result else 1) 