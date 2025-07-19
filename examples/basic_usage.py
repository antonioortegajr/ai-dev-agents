#!/usr/bin/env python3
"""
Basic usage example for AI Dev Agents
"""

import asyncio
import os
import sys
import warnings
from dotenv import load_dotenv

# Suppress warnings for clean output
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.github_mcp_client import GitHubMCPClient
from src.crew_agents import GitHubIssueAgent, SeniorDeveloperAgent

# Load environment variables
load_dotenv()

async def example_usage():
    """Example of how to use the AI Dev Agents system"""
    
    # Configuration
    repository = "microsoft/vscode"  # Example repository
    label = "bug"  # Example label
    
    # MCP server URL
    mcp_url = "http://localhost:3000"
    
    print("🤖 AI Dev Agents - Example Usage")
    print("=" * 60)
    print("Choose example mode:")
    print("1. Analyze issues by label")
    print("2. Handle AI tasks (senior developer)")
    print()
    
    mode = input("Enter your choice (1 or 2): ").strip()
    
    if mode == "2":
        # Senior Developer example
        print(f"\n🤖 Senior Developer Agent - Example")
        print("=" * 60)
        print(f"Repository: {repository}")
        print("Looking for issues labeled as 'ai-task'...")
        print()
        
        try:
            # Create MCP client
            async with GitHubMCPClient(mcp_url) as mcp_client:
                # Test connection
                print("Testing connection to MCP server...")
                
                # Create Senior Developer Agent
                print("🤖 Creating Senior Developer Agent...")
                senior_dev_agent = SeniorDeveloperAgent(mcp_client)
                
                # Handle AI tasks
                print("📊 Starting AI task handling...")
                result = await senior_dev_agent.handle_ai_tasks(repository)
                
                print("\n" + "=" * 60)
                print("AI TASK HANDLING RESULTS")
                print("=" * 60)
                print(result)
                
                # Save implementations if any code was generated
                if "```" in result:
                    print("\n" + "=" * 60)
                    print("SAVING IMPLEMENTATIONS")
                    print("=" * 60)
                    save_result = senior_dev_agent.save_implementations(result)
                    print(save_result)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n💡 Make sure the MCP server is running:")
            print("   python main.py server")
        return
    
    # Default mode - analyze issues by label
    print(f"🔍 Analyzing issues with label '{label}' in {repository}")
    print("=" * 60)
    
    try:
        # Create MCP client
        async with GitHubMCPClient(mcp_url) as mcp_client:
            # Test connection
            print("Testing connection to MCP server...")
            
            # Get both filtered and total issues
            issues = await mcp_client.get_issues_by_label(repository, label)
            all_open_issues = await mcp_client.get_all_open_issues(repository)
            
            print(f"✅ Found {len(issues)} issues with label '{label}'")
            print(f"📊 Total open issues: {len(all_open_issues)}")
            if len(all_open_issues) > 0:
                percentage = (len(issues) / len(all_open_issues) * 100)
                print(f"📈 Percentage: {percentage:.1f}%")
            print()
            
            if issues:
                print("\n📋 Sample issues:")
                for issue in issues[:3]:  # Show first 3 issues
                    print(f"  • #{issue.number}: {issue.title}")
                    print(f"    State: {issue.state}")
                    print(f"    URL: {issue.html_url}")
                    print()
            
            # Create Crew AI agent
            print("🤖 Creating Crew AI agents...")
            agent = GitHubIssueAgent(mcp_client)
            
            # Analyze issues
            print("📊 Starting analysis...")
            result = await agent.analyze_issues_by_label(repository, label)
            
            print("\n" + "=" * 60)
            print("ANALYSIS RESULTS")
            print("=" * 60)
            print(result)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure the MCP server is running:")
        print("   python main.py server")

if __name__ == "__main__":
    asyncio.run(example_usage()) 