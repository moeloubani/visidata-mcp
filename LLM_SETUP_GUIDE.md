# VisiData MCP Setup Guide for LLM Assistants

**Purpose**: This guide is designed for LLM assistants to read and use when helping users set up VisiData MCP server.

**How to use this guide**: When a user asks for setup help, read this entire guide and walk them through the appropriate steps based on their system and preferences.

**📋 Latest Version**: This guide is always up-to-date at: https://github.com/moeloubani/visidata-mcp/blob/main/LLM_SETUP_GUIDE.md

---

## Step 1: System Requirements Check

### Ask the user to run these commands:

```bash
# Check Python version (must be 3.10+)
python3 --version

# Check if they have pipx (recommended)
pipx --version

# Check if they have npm (alternative method)
npm --version
```

### Expected responses:
- **Python 3.10+**: ✅ Proceed
- **Python < 3.10 or not found**: ❌ User needs to install Python 3.10+
- **pipx found**: ✅ Recommend pipx installation
- **pipx not found**: Recommend installing pipx first
- **npm found**: Alternative installation method available

---

## Step 2: Installation Method Selection

### Recommend based on user's system:

#### Option A: pipx Installation (RECOMMENDED)
**When to recommend**: User has Python 3.10+ and either has pipx or can install it

**Steps to guide user through:**

1. **Install pipx if not present:**
   ```bash
   # macOS with Homebrew
   brew install pipx
   
   # Or with pip
   python3 -m pip install --user pipx
   ```

2. **Install visidata-mcp:**
   ```bash
   pipx install visidata-mcp
   ```

3. **Verify installation:**
   ```bash
   # Check if command exists
   which visidata-mcp
   
   # Should show: /Users/[username]/.local/bin/visidata-mcp
   ```

#### Option B: npm Installation
**When to recommend**: User has npm and prefers npm, OR pipx installation fails

**Steps:**
1. **Install the package:**
   ```bash
   npm install -g @moeloubani/visidata-mcp@beta
   ```

2. **Check for issues:**
   ```bash
   # Test the command
   visidata-mcp --help
   ```

**Common issue**: If you see "externally-managed-environment" error, switch to pipx method.

---

## Step 3: Find the Correct Command Path

### CRITICAL: Multiple versions can conflict

**Have user run:**
```bash
# See which version is found first
which visidata-mcp

# List all versions
ls -la ~/.local/bin/visidata-mcp 2>/dev/null || echo "No pipx version"
ls -la ~/.nvm/versions/node/*/bin/visidata-mcp 2>/dev/null || echo "No npm version"
```

### Interpret results:
- **If `which visidata-mcp` shows npm path**: May be broken, check if pipx version exists
- **If `which visidata-mcp` shows pipx path**: Good, should work
- **If multiple versions exist**: Recommend using full path to avoid conflicts

---

## Step 4: Configure MCP Client

### For Cursor AI:

1. **Create configuration file:**
   ```bash
   # Navigate to project directory
   cd /path/to/your/project
   
   # Create .cursor directory if it doesn't exist
   mkdir -p .cursor
   ```

2. **Create `.cursor/mcp.json` with this content:**

   **RECOMMENDED (full path):**
   ```json
   {
     "mcpServers": {
       "visidata": {
         "command": "/Users/[USERNAME]/.local/bin/visidata-mcp"
       }
     }
   }
   ```

   **Alternative (if sure about PATH):**
   ```json
   {
     "mcpServers": {
       "visidata": {
         "command": "visidata-mcp"
       }
     }
   }
   ```

3. **Replace `[USERNAME]`** with their actual username. Get it with: `echo $USER`

### For Claude Desktop:

1. **Find config file location:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

2. **Add to config file:**
   ```json
   {
     "mcpServers": {
       "visidata": {
         "command": "/Users/[USERNAME]/.local/bin/visidata-mcp"
       }
     }
   }
   ```

---

## Step 5: Test the Setup

### Have user test the installation:

1. **Basic test:**
   ```bash
   # Test with MCP Inspector
   npx @modelcontextprotocol/inspector /Users/[USERNAME]/.local/bin/visidata-mcp
   ```

2. **What to expect:**
   - Browser opens with MCP Inspector
   - Shows URL like: `http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=...`
   - Should display 8+ available tools
   - User can test tools in the web interface

3. **If MCP Inspector works:**
   - ✅ Installation is correct
   - ✅ Restart their AI application (Cursor/Claude Desktop)
   - ✅ Look for "Available MCP Tools" in the chat

---

## Troubleshooting Guide

### Problem: "0 tools available" in AI application

**Most common cause**: PATH conflict or wrong command path

**Solution steps:**
1. **Check which version is being used:**
   ```bash
   which visidata-mcp
   ```

2. **If it shows npm version but you want pipx:**
   ```bash
   # Use full path in config
   /Users/[USERNAME]/.local/bin/visidata-mcp
   ```

3. **Verify the chosen version works:**
   ```bash
   # This should NOT hang or error
   echo '{"jsonrpc":"2.0","id":1,"method":"ping"}' | /Users/[USERNAME]/.local/bin/visidata-mcp
   ```

4. **Always restart** the AI application completely after config changes

### Problem: "externally-managed-environment" error

**Cause**: npm version trying to install Python package in protected environment

**Solution**: Switch to pipx installation method (Step 2, Option A)

### Problem: Command hangs or runs forever

**Cause**: MCP servers run indefinitely waiting for JSON-RPC input

**Solution**: This is normal! Use Ctrl+C to stop. Test with MCP Inspector instead.

### Problem: "Python package not found"

**Cause**: Dependencies not installed properly

**Solution**:
1. **For pipx**: Reinstall with `pipx reinstall visidata-mcp`
2. **For npm**: Switch to pipx method
3. **Verify**: `python3 -c "import visidata_mcp; print('OK')"`

---

## Success Indicators

### User should see:
1. ✅ **MCP Inspector shows 8+ tools** (load_data, analyze_data, convert_data, etc.)
2. ✅ **AI application shows "Available MCP Tools"** in chat interface
3. ✅ **Can use tools like**: "Please analyze this CSV file: /path/to/file.csv"
4. ✅ **Tools return data** and don't show errors

### Tools available:
- `load_data` - Load and inspect data files
- `get_data_sample` - Get preview of data  
- `analyze_data` - Comprehensive data analysis
- `convert_data` - Convert between formats
- `filter_data` - Filter data based on conditions
- `get_column_stats` - Get column statistics
- `sort_data` - Sort data by column
- `get_supported_formats` - List supported formats

---

## Quick Reference Commands

### For LLM to copy/paste to user:

```bash
# Check system
python3 --version && pipx --version

# Install (recommended)
pipx install visidata-mcp

# Find path
which visidata-mcp
echo $USER

# Test installation
npx @modelcontextprotocol/inspector ~/.local/bin/visidata-mcp

# Configuration template (Cursor)
mkdir -p .cursor
cat > .cursor/mcp.json << 'EOF'
{
  "mcpServers": {
    "visidata": {
      "command": "/Users/USERNAME/.local/bin/visidata-mcp"
    }
  }
}
EOF
```

**Remember**: Replace `USERNAME` with actual username from `echo $USER`

---

## Final Notes for LLM Assistants

1. **Always ask user to restart** their AI application after configuration
2. **Recommend full paths** to avoid PATH conflicts
3. **Use MCP Inspector for testing** - it's the definitive test
4. **If npm version fails**, immediately switch to pipx
5. **Guide users step by step** - don't assume they know terminal commands
6. **Verify each step** before moving to the next one 