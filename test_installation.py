#!/usr/bin/env python3
"""
Installation test script for AI Dev Agents
"""

import sys
import os

# Suppress warnings for clean output
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import crewai
        print("✅ Crew AI imported successfully")
    except ImportError as e:
        print(f"❌ Crew AI import failed: {e}")
        return False
    
    try:
        import aiohttp
        print("✅ aiohttp imported successfully")
    except ImportError as e:
        print(f"❌ aiohttp import failed: {e}")
        return False
    
    try:
        import pydantic
        print("✅ pydantic imported successfully")
    except ImportError as e:
        print(f"❌ pydantic import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    return True

def test_project_imports():
    """Test that project modules can be imported"""
    print("\n🧪 Testing project imports...")
    
    try:
        from src.github_mcp_client import GitHubMCPClient, GitHubIssue
        print("✅ GitHub MCP Client imported successfully")
    except ImportError as e:
        print(f"❌ GitHub MCP Client import failed: {e}")
        return False
    
    try:
        from src.crew_agents import GitHubIssueAgent
        print("✅ Crew Agents imported successfully")
    except ImportError as e:
        print(f"❌ Crew Agents import failed: {e}")
        return False
    
    try:
        from src.mcp_server import GitHubMCPServer
        print("✅ MCP Server imported successfully")
    except ImportError as e:
        print(f"❌ MCP Server import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment setup"""
    print("\n🧪 Testing environment...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 9):
        print("❌ Python 3.9+ is required")
        return False
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found (you'll need to create one)")
    
    return True

def main():
    """Run all tests"""
    print("🤖 AI Dev Agents - Installation Test")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test project imports
    if not test_project_imports():
        all_passed = False
    
    # Test environment
    if not test_environment():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! Your installation is ready.")
        print("\nNext steps:")
        print("1. Copy env.example to .env and configure your settings")
        print("2. Run: python main.py server (to start MCP server)")
        print("3. Run: python main.py (to start the application)")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure you're using Python 3.9+")
        print("2. Try: pip install -r requirements.txt --force-reinstall")
        print("3. Check the README.md for more details")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 