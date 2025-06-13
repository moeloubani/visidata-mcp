#!/usr/bin/env python3
"""Test script to check MCP server tools registration."""

import asyncio
from visidata_mcp.server import mcp

async def test_tools():
    """Test if tools are registered properly."""
    try:
        tools = await mcp.list_tools()
        print(f"Number of tools registered: {len(tools)}")
        print("\nRegistered tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
            
        resources = await mcp.list_resources()
        print(f"\nNumber of resources registered: {len(resources)}")
        for resource in resources:
            print(f"  - {resource.uri}: {resource.name}")
            
        prompts = await mcp.list_prompts()
        print(f"\nNumber of prompts registered: {len(prompts)}")
        for prompt in prompts:
            print(f"  - {prompt.name}: {prompt.description}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_tools()) 