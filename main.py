#!/usr/bin/env python3
"""
Main application for AI Dev Agents using Crew AI and GitHub MCP Server
"""

import asyncio
import logging
from dotenv import load_dotenv

# Import warning suppression first
from src.warning_suppression import configure_logging, suppress_warnings

# Suppress warnings before importing other modules
suppress_warnings()

from src.github_mcp_client import GitHubMCPClient
from src.crew_agents import GitHubIssueAgent, SeniorDeveloperAgent

# Load environment variables
load_dotenv()

# Configure logging with warning suppression
configure_logging(level=logging.INFO, suppress_warnings_flag=True)
logger = logging.getLogger(__name__)

async def main():
    """Main function to demonstrate the GitHub issue analysis"""
    
    # Check required environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    repository = os.getenv("GITHUB_REPOSITORY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not github_token:
        logger.error("GITHUB_TOKEN environment variable is required")
        return
    
    if not repository:
        logger.error("GITHUB_REPOSITORY environment variable is required (format: owner/repo)")
        return
    
    if not openai_api_key:
        logger.error("OPENAI_API_KEY environment variable is required")
        return
    
    # Set OpenAI API key for Crew AI
    os.environ["OPENAI_API_KEY"] = openai_api_key
    
    # MCP server configuration
    mcp_host = os.getenv("MCP_SERVER_HOST", "localhost")
    mcp_port = int(os.getenv("MCP_SERVER_PORT", "3000"))
    mcp_url = f"http://{mcp_host}:{mcp_port}"
    
    print("🤖 AI Dev Agents - GitHub Issue Analysis")
    print("=" * 50)
    print(f"Repository: {repository}")
    print(f"MCP Server: {mcp_url}")
    print()
    
    # Choose operation mode
    print("Choose operation mode:")
    print("1. Analyze issues by label")
    print("2. Handle AI tasks (senior developer)")
    print()
    
    mode = input("Enter your choice (1 or 2): ").strip()
    
    if mode == "2":
        # Senior Developer mode - handle AI tasks
        print(f"\n🤖 Senior Developer Agent - Handling AI Tasks")
        print("=" * 50)
        print(f"Repository: {repository}")
        print("Looking for issues labeled as 'ai-task'...")
        print()
        
        try:
            # Create MCP client
            async with GitHubMCPClient(mcp_url) as mcp_client:
                # Test connection to MCP server
                print("Testing MCP server connection...")
                
                # Create Senior Developer Agent
                senior_dev_agent = SeniorDeveloperAgent(mcp_client)
                
                # Handle AI tasks
                print("Starting Senior Developer analysis...")
                result = await senior_dev_agent.handle_ai_tasks(repository)
                
                print("\n" + "=" * 50)
                print("AI TASK HANDLING RESULTS")
                print("=" * 50)
                print(result)
                
                # Save implementations if any code was generated
                if "```" in result:
                    print("\n" + "=" * 50)
                    print("SAVING IMPLEMENTATIONS")
                    print("=" * 50)
                    save_result = senior_dev_agent.save_implementations(result)
                    print(save_result)
                
        except Exception as e:
            logger.error(f"Error in senior developer mode: {e}")
            print(f"Error: {e}")
            print("\nMake sure the MCP server is running with:")
            print("python src/mcp_server.py")
        return
    
    # Default mode - analyze issues by label
    label = input("Enter the label to filter issues by: ").strip()
    if not label:
        print("No label provided. Using 'bug' as default.")
        label = "bug"
    
    print(f"\nAnalyzing issues with label '{label}' in {repository}...")
    print()
    
    try:
        # Create MCP client
        async with GitHubMCPClient(mcp_url) as mcp_client:
            # Test connection to MCP server
            print("Testing MCP server connection...")
            
            # Get both filtered and total issues
            test_issues = await mcp_client.get_issues_by_label(repository, label)
            all_open_issues = await mcp_client.get_all_open_issues(repository)
            
            print(f"📊 Repository Statistics:")
            print(f"   Total open issues: {len(all_open_issues)}")
            print(f"   Issues with label '{label}': {len(test_issues)}")
            if len(all_open_issues) > 0:
                percentage = (len(test_issues) / len(all_open_issues) * 100)
                print(f"   Percentage: {percentage:.1f}%")
            print()
            
            # Create Crew AI agent
            agent = GitHubIssueAgent(mcp_client)
            
            # Analyze issues
            print("Starting Crew AI analysis...")
            result = await agent.analyze_issues_by_label(repository, label)
            
            print("\n" + "=" * 50)
            print("ANALYSIS RESULTS")
            print("=" * 50)
            print(result)
            
    except Exception as e:
        logger.error(f"Error in main application: {e}")
        print(f"Error: {e}")
        print("\nMake sure the MCP server is running with:")
        print("python src/mcp_server.py")

async def run_mcp_server():
    """Run the MCP server"""
    from src.mcp_server import main as mcp_main
    await mcp_main()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        # Run MCP server
        print("Starting MCP server...")
        asyncio.run(run_mcp_server())
    else:
        # Run main application
        asyncio.run(main()) 
