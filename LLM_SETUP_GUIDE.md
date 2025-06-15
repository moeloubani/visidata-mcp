# VisiData MCP Setup Guide for LLM Assistants

**Purpose**: This guide helps LLM assistants walk users through setting up VisiData MCP server with their AI application.

**📋 Latest Version**: https://github.com/moeloubani/visidata-mcp/blob/main/LLM_SETUP_GUIDE.md

---

## ⚠️ IMPORTANT: DO NOT CLONE THE REPOSITORY

**Users do NOT need to:**
- Clone or download the GitHub repository
- Install from source
- Run any setup scripts

**Users ONLY need to:**
1. Install the npm package globally
2. Configure their AI application

---

## 📋 Summary for LLM Assistants

**When a user asks for help setting up VisiData MCP:**

1. **Run the install command for them**: `npm install -g @moeloubani/visidata-mcp`
2. **Ask which AI app they use**: Cursor, Windsurf, or Claude Desktop
3. **Create the config file** for their specific app
4. **Tell them to restart** their AI application completely

**That's it! No cloning, no complex setup, just install + configure + restart.**

---

## Simple 2-Step Process

### Step 1: Install VisiData MCP

**Run this command for the user:**
```bash
npm install -g @moeloubani/visidata-mcp
```

**This installs the package globally on their system - no cloning needed!**

**What to expect:**
- ✅ Downloads and installs the package
- ✅ May show warnings about Python - this is normal
- ✅ Creates global `visidata-mcp` command

**If they get an error:**
- **"npm not found"**: They need to install Node.js first from https://nodejs.org
- **Permission errors**: They may need `sudo npm install -g @moeloubani/visidata-mcp`

---

### Step 2: Configure Their AI Application

**Ask which AI application they're using, then help them create ONE config file:**

**IMPORTANT**: Users need to create a config file in their project directory (for Cursor/Windsurf) or system config location (for Claude Desktop). They do NOT need to clone anything.

#### For Cursor AI

1. **Navigate to their project directory**
2. **Create the configuration directory and file:**
   ```bash
   mkdir -p .cursor
   ```

3. **Create `.cursor/mcp.json` with this content:**
   ```json
   {
     "mcpServers": {
       "visidata": {
         "command": "visidata-mcp"
       }
     }
   }
   ```

4. **Tell them to restart Cursor completely** (Cmd+Q and reopen)

#### For Windsurf

1. **Navigate to their project directory**
2. **Create the configuration directory and file:**
   ```bash
   mkdir -p .windsurf
   ```

3. **Create `.windsurf/mcp.json` with this content:**
   ```json
   {
     "mcpServers": {
       "visidata": {
         "command": "visidata-mcp"
       }
     }
   }
   ```

4. **Tell them to restart Windsurf completely**

#### For Claude Desktop

1. **Find their config file location:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

2. **Add this to the config file:**
   ```json
   {
     "mcpServers": {
       "visidata": {
         "command": "visidata-mcp"
       }
     }
   }
   ```

3. **Restart Claude Desktop**

---

## Testing the Setup

**Ask the user to:**

1. **Restart their AI application** completely
2. **Look for "Available MCP Tools"** or similar indicator in the chat interface
3. **Try a simple test:** "Please analyze this data file: [path to a CSV file]"

**Success indicators:**
- ✅ AI application shows MCP tools are available
- ✅ Can use commands like: load_data, analyze_data, convert_data
- ✅ No "0 tools available" errors

---

## Troubleshooting

### "0 tools available"

**Most common cause**: Configuration not applied properly

**Solutions:**
1. **Double-check the config file path** and content
2. **Restart the AI application completely** (not just reload)
3. **Check the command works:** Run `visidata-mcp --version` in terminal

### "Command not found: visidata-mcp"

**Cause**: npm package not installed globally or PATH issue

**Solutions:**
1. **Reinstall:** `npm install -g @moeloubani/visidata-mcp`
2. **Check global npm packages:** `npm list -g @moeloubani/visidata-mcp`
3. **Check PATH:** Make sure npm global bin is in PATH

### "Python package not found" or similar errors

**Cause**: The npm package automatically installs Python dependencies

**Solutions:**
1. **Let it finish:** The first run may take a moment to set up Python packages
2. **Check Python:** Make sure Python 3.10+ is installed
3. **Manual install:** If needed, run `pip install visidata-mcp`

---

## Quick Reference Commands

### Installation
```bash
# Install the package
npm install -g @moeloubani/visidata-mcp

# Verify installation
visidata-mcp --version

# Check if npm global packages are in PATH
npm list -g @moeloubani/visidata-mcp
```

### Configuration Templates

**Cursor (.cursor/mcp.json):**
```json
{
  "mcpServers": {
    "visidata": {
      "command": "visidata-mcp"
    }
  }
}
```

**Windsurf (.windsurf/mcp.json):**
```json
{
  "mcpServers": {
    "visidata": {
      "command": "visidata-mcp"
    }
  }
}
```

**Claude Desktop:**
```json
{
  "mcpServers": {
    "visidata": {
      "command": "visidata-mcp"
    }
  }
}
```

---

## Available Tools

Once set up, users will have access to these data analysis tools:

- **load_data** - Load and inspect data files
- **get_data_sample** - Preview data 
- **analyze_data** - Comprehensive data analysis
- **convert_data** - Convert between formats (CSV, JSON, Excel, etc.)
- **filter_data** - Filter data based on conditions
- **sort_data** - Sort data by columns
- **get_column_stats** - Get statistics for specific columns
- **get_supported_formats** - List all supported file formats

---

## Notes for LLM Assistants

1. **NO CLONING**: Users never need to clone the GitHub repository
2. **Run commands for them**: Use terminal tools to run `npm install` and create config files
3. **One config file**: Create ONE config file for their specific AI app
4. **Always restart**: Emphasize completely restarting the AI application
5. **Keep it simple**: Don't mention source installation, pipx, or other methods
6. **Test with real data**: Suggest they try with an actual CSV file they have 