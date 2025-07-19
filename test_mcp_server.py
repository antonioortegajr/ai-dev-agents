#!/usr/bin/env python3
"""
Test script for MCP server functionality
"""

import asyncio
import json
import logging
from unittest.mock import AsyncMock, patch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_mcp_server():
    """Test the MCP server functionality"""
    
    print("🧪 Testing MCP Server Functionality")
    print("=" * 40)
    
    # Test 1: Check if we can create the server
    try:
        from src.mcp_server import GitHubMCPServer, MCPHandler, MCPRequest, MCPResponse
        print("✅ MCP Server classes imported successfully")
    except Exception as e:
        print(f"❌ Failed to import MCP Server classes: {e}")
        return False
    
    # Test 2: Test GitHubMCPServer session management
    try:
        # Mock the GitHub token
        server = GitHubMCPServer("test_token")
        
        # Test session initialization
        await server.__aenter__()
        print("✅ Session initialized successfully")
        
        # Test session cleanup
        await server.__aexit__(None, None, None)
        print("✅ Session cleaned up successfully")
        
    except Exception as e:
        print(f"❌ Failed to test session management: {e}")
        return False
    
    # Test 3: Test MCP request/response models
    try:
        request = MCPRequest(
            method="github.list_issues",
            params={"owner": "test", "repo": "test", "labels": ["bug"]}
        )
        response = MCPResponse(result={"issues": []})
        print("✅ MCP request/response models work correctly")
        
    except Exception as e:
        print(f"❌ Failed to test MCP models: {e}")
        return False
    
    print("\n🎉 All MCP Server tests passed!")
    print("\nTo test with real GitHub API:")
    print("1. Set GITHUB_TOKEN environment variable")
    print("2. Run: python src/mcp_server.py")
    print("3. In another terminal, test with: curl -X POST http://localhost:3000/call")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    exit(0 if success else 1) 