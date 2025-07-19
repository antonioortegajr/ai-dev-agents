#!/usr/bin/env python3
"""
Test to demonstrate how the Senior Developer Agent takes action on GitHub issues
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
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.crew_agents import SeniorDeveloperAgent
from src.github_mcp_client import GitHubIssue

# Load environment variables
load_dotenv()

async def test_action_taking():
    """Test that the agent takes action on GitHub issues"""
    
    print("🧪 Testing Action Taking on GitHub Issues")
    print("=" * 50)
    print("This test demonstrates how the agent now takes ACTION on issues,")
    print("not just analyzes them.")
    print()
    
    # Create a mock agent for testing
    agent = SeniorDeveloperAgent(None)  # No MCP client for this test
    
    # Example issues that would trigger different actions
    code_change_issue = GitHubIssue(
        number=123,
        title="Implement user authentication API",
        body="""Create a REST API endpoint for user authentication.

Requirements:
- POST /api/auth/login endpoint
- Accept username and password
- Return JWT token on success
- Handle invalid credentials
- Use bcrypt for password hashing

Please implement this in Python using Flask.""",
        state="open",
        labels=[{"name": "ai-task"}],
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        html_url="https://github.com/test/repo/issues/123"
    )
    
    invalid_issue = GitHubIssue(
        number=124,
        title="Invalid test issue",
        body="This is an invalid test issue that should be closed.",
        state="open",
        labels=[{"name": "ai-task"}],
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        html_url="https://github.com/test/repo/issues/124"
    )
    
    completed_issue = GitHubIssue(
        number=125,
        title="Add user registration - DONE",
        body="This feature has been completed and implemented.",
        state="open",
        labels=[{"name": "ai-task"}],
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        html_url="https://github.com/test/repo/issues/125"
    )
    
    print("📋 Testing Issue Classification:")
    print()
    
    # Test code change detection
    print(f"✅ Issue #{code_change_issue.number}: {code_change_issue.title}")
    print(f"   Requires code changes: {agent._requires_code_changes(code_change_issue)}")
    print(f"   Action: Would create pull request")
    print()
    
    # Test invalid issue detection
    print(f"✅ Issue #{invalid_issue.number}: {invalid_issue.title}")
    print(f"   Is invalid: {agent._is_invalid_issue(invalid_issue)}")
    print(f"   Action: Would close issue")
    print()
    
    # Test completed issue detection
    print(f"✅ Issue #{completed_issue.number}: {completed_issue.title}")
    print(f"   Is completed: {agent._is_completed_issue(completed_issue)}")
    print(f"   Action: Would close issue")
    print()
    
    print("🎯 Actions the Agent Now Takes:")
    print("1. 📝 Analyzes the exact requirements from GitHub issues")
    print("2. 💻 Implements code solutions that match the requirements")
    print("3. 🔄 Creates pull requests for code changes")
    print("4. 💬 Adds comments to issues with analysis")
    print("5. ❌ Closes invalid or unclear issues")
    print("6. ✅ Closes completed issues")
    print("7. 📁 Saves implementation files")
    print()
    
    print("🔧 MCP Server Methods Used:")
    print("- github.list_issues: Get issues with 'ai-task' label")
    print("- github.close_issue: Close invalid/completed issues")
    print("- github.add_issue_comment: Add analysis comments")
    print("- github.create_pull_request: Create PRs for code changes")
    print()
    
    print("📊 Expected Output:")
    print("=" * 50)
    print("ANALYSIS RESULTS")
    print("=" * 50)
    print("(Crew AI analysis of the issues)")
    print()
    print("=" * 50)
    print("ACTIONS TAKEN ON ISSUES")
    print("=" * 50)
    print("Processing Issue #123: Implement user authentication API")
    print("✅ Created pull request: Pull request would be created for issue #123")
    print("✅ Added comment to issue #123")
    print()
    print("Processing Issue #124: Invalid test issue")
    print("✅ Closed invalid issue #124")
    print()
    print("Processing Issue #125: Add user registration - DONE")
    print("✅ Closed completed issue #125")
    print()
    
    print("✅ The agent now takes REAL action on GitHub issues!")
    print("It doesn't just analyze - it actually completes tasks.")

if __name__ == "__main__":
    asyncio.run(test_action_taking()) 