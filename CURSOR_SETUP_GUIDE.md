# VisiData MCP Setup for Cursor

## 🎯 **Quick Setup**

### **✅ CORRECT MCP Server Path**
```
/Users/moe/Dev/visidata-mcp/venv/bin/visidata-mcp
```

### **❌ WRONG PATH** (old pipx version)
```
/Users/moe/.local/pipx/venvs/visidata-mcp/bin/visidata-mcp
```

## ⚙️ **Configuration**

### **For Claude Desktop**
File: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "visidata-local": {
      "command": "/Users/moe/Dev/visidata-mcp/venv/bin/python",
      "args": ["-m", "visidata_mcp.server"],
      "cwd": "/Users/moe/Dev/visidata-mcp",
      "env": {
        "PYTHONPATH": "/Users/moe/Dev/visidata-mcp/src"
      }
    }
  }
}
```

### **For Cursor**
Create `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "visidata-local": {
      "command": "/Users/moe/Dev/visidata-mcp/venv/bin/visidata-mcp",
      "args": [],
      "env": {
        "PYTHONPATH": "/Users/moe/Dev/visidata-mcp/src"
      }
    }
  }
}
```

## 🔧 **Verification**

```bash
cd /Users/moe/Dev/visidata-mcp
source venv/bin/activate
python -c "from visidata_mcp.server import main; print('✅ Server ready')"
python -c "import matplotlib, seaborn, scipy; print('✅ All deps available')"
```

## 🚨 **Troubleshooting**

**If you get "No module named 'matplotlib'":**

1. **Check which server is running:**
   ```bash
   ps aux | grep visidata-mcp
   ```

2. **Verify you're using the local path:**
   - ✅ Should contain: `/Users/moe/Dev/visidata-mcp/venv/`
   - ❌ Should NOT contain: `/Users/moe/.local/pipx/`

3. **Restart Cursor/Claude Desktop** after changing config

4. **Verify local installation:**
   ```bash
   cd /Users/moe/Dev/visidata-mcp
   source venv/bin/activate
   pip list | grep matplotlib  # Should show matplotlib 3.10.3
   ```

## 🎉 **Available Features**

Once connected, you'll have access to:

### **✅ Visualization Functions**
- `create_correlation_heatmap()` - Correlation matrices
- `create_distribution_plots()` - Statistical distribution plots  
- `create_graph()` - Custom graphs (scatter, line, bar, histogram)

### **🆕 Skills Analysis Functions**
- `parse_skills_column()` - Parse comma-separated skills
- `analyze_skills_by_location()` - Skills analysis by location
- `create_skills_location_heatmap()` - Skills distribution heatmap
- `analyze_salary_by_location_and_skills()` - Comprehensive salary analysis

## 📊 **Test Commands**

```
# Test correlation heatmap
Use the VisiData MCP to create a correlation heatmap from examples/sample_data.csv

# Test skills analysis  
Use the VisiData MCP to analyze skills by location from examples/ai_job_dataset.csv using the 'required_skills' and 'company_location' columns
``` 