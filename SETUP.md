# VisiData MCP Server Setup Guide

This guide will help you install and configure the VisiData MCP server for use with Claude Desktop and other MCP clients.

## Prerequisites

Before installing the VisiData MCP server, ensure you have:

- **Python 3.8 or higher** installed on your system
- **pip** (Python package installer)
- **VisiData 3.0 or higher** (will be installed as a dependency)

## Installation

### Method 1: Install from PyPI (Recommended)

```bash
pip install visidata-mcp
```

### Method 2: Install from Source

1. Clone the repository:
```bash
git clone https://github.com/your-username/visidata-mcp.git
cd visidata-mcp
```

2. Install the package:
```bash
pip install -e .
```

### Method 3: Development Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/visidata-mcp.git
cd visidata-mcp
```

2. Install in development mode:
```bash
pip install -e .
pip install -r requirements.txt
```

## Verification

Test your installation:

```bash
# Run the test script
python test_server.py

# Or test individual components
python -c "from visidata_mcp.server import get_supported_formats; print('✓ Installation successful')"
```

## Configuration

### Claude Desktop Integration

#### macOS Configuration

1. Open the Claude Desktop configuration file:
```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. Add the VisiData MCP server configuration:
```json
{
  "mcpServers": {
    "visidata": {
      "command": "visidata-mcp"
    }
  }
}
```

#### Windows Configuration

1. Open the Claude Desktop configuration file:
```
%APPDATA%\Claude\claude_desktop_config.json
```

2. Add the same configuration as above.

#### Development/Source Installation Configuration

**⚠️ IMPORTANT**: For development installations or virtual environments, you **must** use the full path to your virtual environment's Python executable:

```json
{
  "mcpServers": {
    "visidata": {
      "command": "/full/path/to/your/visidata-mcp/venv/bin/python",
      "args": ["-m", "visidata_mcp.server"],
      "cwd": "/full/path/to/your/visidata-mcp"
    }
  }
}
```

**Example for macOS/Linux**:
```json
{
  "mcpServers": {
    "visidata": {
      "command": "/Users/username/Dev/visidata-mcp/venv/bin/python",
      "args": ["-m", "visidata_mcp.server"],
      "cwd": "/Users/username/Dev/visidata-mcp"
    }
  }
}
```

**Why the full path is required**:
- Ensures the correct Python interpreter with all dependencies is used
- Avoids PATH-related issues that can cause "0 tools available" errors
- Works consistently across different system configurations

### Environment Variables (Optional)

You can set these environment variables to customize behavior:

```bash
# Set VisiData options
export VD_BATCH=1              # Run in batch mode
export VD_CONFIRM_OVERWRITE=0  # Don't ask for confirmations

# Set MCP options
export MCP_LOG_LEVEL=DEBUG     # Enable debug logging
```

## Testing the Installation

### 1. Basic Server Test

```bash
# Run the included test script
python test_server.py
```

Expected output:
```
Testing VisiData MCP Server...

1. Testing basic functionality...
✓ Successfully imported VisiData MCP server functions
✓ get_supported_formats() works correctly
✓ load_data() works correctly
✓ get_data_sample() works correctly
✓ analyze_data() works correctly
   Basic functionality test: PASSED

2. Testing server startup...
✓ MCP server object created successfully
✓ Tools appear to be registered
   Server startup test: PASSED

Results: 2/2 tests passed
🎉 All tests passed! The VisiData MCP server appears to be working correctly.
```

### 2. Demo with Sample Data

```bash
# Run the demo script
cd examples
python demo.py
```

This will demonstrate all the server's capabilities using the included sample data.

### 3. MCP Inspector (Development)

For debugging and development:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run with inspector
npx @modelcontextprotocol/inspector visidata-mcp
```

## Troubleshooting

### Common Issues and Solutions

#### 1. "0 tools available" or "No MCP tools found"

**Symptoms**: Cursor or Claude Desktop shows no available tools

**Solutions**:
1. **Check your MCP configuration path**:
   ```bash
   # Verify the Python path exists
   ls -la /path/to/your/visidata-mcp/venv/bin/python
   ```

2. **Use the absolute path to Python**:
   ```json
   {
     "mcpServers": {
       "visidata": {
         "command": "/full/absolute/path/to/venv/bin/python",
         "args": ["-m", "visidata_mcp.server"],
         "cwd": "/full/absolute/path/to/visidata-mcp"
       }
     }
   }
   ```

3. **Restart your MCP client completely** (not just reload)

#### 2. VisiData Warning Messages

**Symptoms**: You see warnings like:
```
setting unknown option confirm_overwrite
RuntimeWarning: 'visidata_mcp.server' found in sys.modules
```

**Solution**: These warnings are **harmless** and don't affect functionality. They occur because:
- VisiData sets configuration options that may vary between versions
- Python's module loading system issues warnings about import order

#### 3. Server Startup Errors

**Symptoms**: Server fails to start or crashes immediately

**Solutions**:
1. **Test the server manually**:
   ```bash
   cd /path/to/visidata-mcp
   source venv/bin/activate
   python -m visidata_mcp.server
   ```

2. **Check dependencies**:
   ```bash
   pip list | grep -E "(visidata|mcp|pandas)"
   ```

3. **Verify Python version**:
   ```bash
   python --version  # Should be 3.8+
   ```

#### 4. Import Errors

**Symptoms**: `ImportError` or `ModuleNotFoundError`

**Solutions**:
1. **Reinstall the package**:
   ```bash
   cd /path/to/visidata-mcp
   source venv/bin/activate
   pip install -e .
   ```

2. **Check virtual environment activation**:
   ```bash
   which python  # Should point to venv/bin/python
   ```

#### 5. File Permission Issues

**Symptoms**: Permission denied errors

**Solutions**:
1. **Check file permissions**:
   ```bash
   ls -la /path/to/visidata-mcp/venv/bin/python
   chmod +x /path/to/visidata-mcp/venv/bin/python
   ```

2. **Verify directory permissions**:
   ```bash
   ls -la /path/to/visidata-mcp/
   ```

### Verification Commands

Run these commands to verify your installation:

```bash
# 1. Check if the package is installed
cd /path/to/visidata-mcp
source venv/bin/activate
python -c "import visidata_mcp; print('✓ Package imported successfully')"

# 2. Check if tools are registered
python test_tools.py

# 3. Test server startup
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | python -m visidata_mcp.server

# 4. Check virtual environment
which python
python --version
pip list | grep visidata
```

**Expected Results**:
- Package imports without errors
- Test shows "8 tools registered"
- Server responds with JSON initialization response
- Python path points to your virtual environment
- visidata and visidata-mcp packages are listed

### Automated Verification

For a comprehensive check of your entire setup:
```bash
cd /path/to/visidata-mcp
source venv/bin/activate
python verify_setup.py
```

This script will automatically:
- ✅ Check Python version and virtual environment
- ✅ Verify all required packages are installed  
- ✅ Test MCP server tools registration (8 tools expected)
- ✅ Validate MCP configuration files
- ✅ Test server startup and MCP protocol response
- 🔧 Provide specific recommendations for any issues found

## Usage Examples

### Basic Data Loading

Once configured with Claude Desktop, you can use commands like:

```
"Load the data from /path/to/my/data.csv and show me the first 5 rows"
```

The AI will use the VisiData MCP server to:
1. Load the CSV file
2. Extract the first 5 rows
3. Present the data in a readable format

### Data Analysis

```
"Analyze the dataset at /path/to/sales.xlsx and give me statistics for the revenue column"
```

The AI will:
1. Load the Excel file
2. Analyze the overall structure
3. Generate detailed statistics for the revenue column
4. Provide insights about the data

### Data Transformation

```
"Convert the CSV file at /path/to/data.csv to JSON format and save it as output.json"
```

The AI will:
1. Load the CSV data
2. Convert it to JSON format
3. Save the result to the specified file

## Troubleshooting

### Common Issues

#### 1. Import Error: "No module named 'visidata'"

**Solution**: Install VisiData:
```bash
pip install visidata>=3.0
```

#### 2. Import Error: "No module named 'mcp'"

**Solution**: Install the MCP SDK:
```bash
pip install mcp>=1.9.0
```

#### 3. Permission Denied Errors

**Solution**: Ensure the server has read/write permissions for the data directory:
```bash
chmod 755 /path/to/data/directory
```

#### 4. Claude Desktop Not Recognizing Server

**Solutions**:
1. Check the configuration file syntax with a JSON validator
2. Restart Claude Desktop after configuration changes
3. Verify the server path is correct
4. Check Claude Desktop logs for error messages

#### 5. Large File Processing Issues

**Solutions**:
1. VisiData handles large files efficiently, but ensure adequate system memory
2. Use data sampling for initial exploration of very large datasets
3. Consider filtering or sorting operations to reduce dataset size

### Debug Mode

Enable debug logging:

```bash
# Set environment variable
export MCP_LOG_LEVEL=DEBUG

# Run server with debug output
python -m visidata_mcp.server
```

### Logs Location

- **Claude Desktop Logs**: Check Claude Desktop's console/log output
- **Server Logs**: Use the debug mode above to see server-side logs
- **VisiData Logs**: VisiData errors will be included in tool responses

## Advanced Configuration

### Custom VisiData Settings

Create a `.visidatarc` file in your home directory:

```python
# ~/.visidatarc
import visidata as vd

# Set custom options
vd.options.batch = True
vd.options.confirm_overwrite = False
vd.options.header = 1

# Add custom column types or functions
# (Advanced VisiData configuration)
```

### Resource Limits

For production use, consider setting resource limits:

```json
{
  "mcpServers": {
    "visidata": {
      "command": "visidata-mcp",
      "env": {
        "PYTHONPATH": "/path/to/your/python/env",
        "VD_MAX_ROWS": "1000000"
      }
    }
  }
}
```

## Getting Help

### Documentation

- [VisiData Documentation](https://visidata.org/docs/)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io)
- [VisiData MCP Server README](README.md)

### Support Channels

- **GitHub Issues**: Report bugs and feature requests
- **VisiData Community**: For VisiData-specific questions
- **MCP Community**: For Model Context Protocol questions

### FAQ

**Q: Can I use this with other MCP clients besides Claude Desktop?**
A: Yes, the server implements the standard MCP protocol and should work with any compliant MCP client.

**Q: What's the maximum file size supported?**
A: VisiData can handle very large files (millions of rows), limited primarily by system memory and disk space.

**Q: Can I extend the server with custom tools?**
A: Yes, the server is designed to be extensible. You can add custom tools by modifying the server code.

**Q: Does it support remote data sources?**
A: Currently, the server focuses on local file access. Remote data source support could be added in future versions.

## Next Steps

1. **Explore the Examples**: Run the demo script to see all capabilities
2. **Try with Your Data**: Use the server with your own datasets
3. **Customize**: Modify the server to add domain-specific functionality
4. **Contribute**: Submit improvements and bug fixes to the project

## Security Considerations

- The server has file system access as configured
- Be cautious with file paths when using in production
- Consider running in a sandboxed environment for untrusted data
- Review and validate all file operations

---

*This setup guide covers the essential steps to get started with the VisiData MCP server. For advanced use cases and customization, refer to the source code and VisiData documentation.* 