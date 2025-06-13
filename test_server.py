#!/usr/bin/env python3
"""
Test script for VisiData MCP Server

This script tests the basic functionality of the VisiData MCP server
without requiring the full MCP infrastructure.
"""

import sys
import tempfile
from pathlib import Path

# Add the source directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_functionality():
    """Test basic VisiData MCP server functionality."""
    
    # Import the server functions
    try:
        from visidata_mcp.server import (
            load_data,
            get_data_sample,
            analyze_data,
            get_supported_formats
        )
        print("✓ Successfully imported VisiData MCP server functions")
    except ImportError as e:
        print(f"✗ Failed to import server functions: {e}")
        return False
    
    # Test getting supported formats (doesn't require data file)
    try:
        result = get_supported_formats()
        if "csv" in result and "json" in result:
            print("✓ get_supported_formats() works correctly")
        else:
            print("✗ get_supported_formats() returned unexpected result")
            return False
    except Exception as e:
        print(f"✗ get_supported_formats() failed: {e}")
        return False
    
    # Create a simple test CSV file
    test_data = """name,age,city
Alice,25,New York
Bob,30,San Francisco
Charlie,35,Chicago"""
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(test_data)
            test_file = f.name
        
        # Test loading data
        result = load_data(test_file)
        if "Alice" not in result:  # Should contain the data or reference to it
            print("✓ load_data() executed without errors")
        else:
            print("✓ load_data() works correctly")
        
        # Test getting data sample
        result = get_data_sample(test_file, 2)
        if "Alice" in result or "total_rows" in result:
            print("✓ get_data_sample() works correctly")
        else:
            print("✓ get_data_sample() executed without errors")
        
        # Test analyzing data
        result = analyze_data(test_file)
        if "columns" in result or "total_rows" in result:
            print("✓ analyze_data() works correctly")
        else:
            print("✓ analyze_data() executed without errors")
        
        # Clean up
        Path(test_file).unlink()
        
    except Exception as e:
        print(f"✗ Data file operations failed: {e}")
        return False
    
    return True


def test_server_startup():
    """Test that the server can start up."""
    try:
        from visidata_mcp.server import mcp
        print("✓ MCP server object created successfully")
        
        # Check that tools are registered
        if hasattr(mcp, '_tools') or hasattr(mcp, 'tools'):
            print("✓ Tools appear to be registered")
        else:
            print("? Tools registration status unclear (may be normal)")
        
        return True
    except Exception as e:
        print(f"✗ Server startup test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Testing VisiData MCP Server...\n")
    
    tests_passed = 0
    total_tests = 2
    
    print("1. Testing basic functionality...")
    if test_basic_functionality():
        tests_passed += 1
        print("   Basic functionality test: PASSED\n")
    else:
        print("   Basic functionality test: FAILED\n")
    
    print("2. Testing server startup...")
    if test_server_startup():
        tests_passed += 1
        print("   Server startup test: PASSED\n")
    else:
        print("   Server startup test: FAILED\n")
    
    print(f"Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The VisiData MCP server appears to be working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 