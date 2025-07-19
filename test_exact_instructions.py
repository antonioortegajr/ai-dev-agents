#!/usr/bin/env python3
"""
Test to demonstrate how the Senior Developer Agent follows exact instructions
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

async def test_exact_instructions():
    """Test that the agent follows exact instructions from GitHub issues"""
    
    print("🧪 Testing Exact Instructions Following")
    print("=" * 50)
    print("This test demonstrates how the agent should follow EXACT instructions")
    print("from GitHub issues, not create imaginary tasks.")
    print()
    
    # Example of a real GitHub issue with specific instructions
    example_issue = GitHubIssue(
        number=123,
        title="Create a simple calculator function",
        body="""Create a Python function called `calculate` that takes two numbers and an operator.

Requirements:
- Function name must be exactly `calculate`
- Takes 3 parameters: num1, num2, operator
- Operator can be '+', '-', '*', '/'
- Returns the result of the calculation
- Handle division by zero error
- Function should be in a file called `calculator.py`

Example usage:
calculate(5, 3, '+') should return 8
calculate(10, 2, '/') should return 5.0

Do NOT add any extra features like GUI, web interface, or advanced math functions.
Only implement exactly what is requested.""",
        state="open",
        labels=[{"name": "ai-task"}],
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        html_url="https://github.com/test/repo/issues/123"
    )
    
    print("📋 Example GitHub Issue:")
    print(f"  Issue #{example_issue.number}: {example_issue.title}")
    print(f"  Labels: {', '.join([label['name'] for label in example_issue.labels])}")
    print(f"  State: {example_issue.state}")
    print()
    print("📝 EXACT REQUIREMENTS:")
    print(example_issue.body)
    print()
    
    print("✅ Expected Agent Behavior:")
    print("1. Read the EXACT requirements from the issue")
    print("2. Implement ONLY what is specifically requested")
    print("3. Create a function named exactly 'calculate'")
    print("4. Put it in a file called 'calculator.py'")
    print("5. Handle the specific operators mentioned")
    print("6. Include division by zero error handling")
    print("7. Do NOT add GUI, web interface, or extra features")
    print()
    
    print("❌ What the agent should NOT do:")
    print("- Create imaginary requirements")
    print("- Add features not mentioned in the issue")
    print("- Suggest a different function name")
    print("- Add web interface or GUI")
    print("- Implement advanced math functions")
    print("- Create multiple files unless requested")
    print()
    
    print("🎯 Key Principles:")
    print("- Follow the EXACT instructions from the GitHub issue")
    print("- Implement ONLY what is explicitly requested")
    print("- Do not add features or requirements not mentioned")
    print("- Do not make assumptions about what the user wants")
    print("- Stick to the specifications precisely as written")
    print()
    
    print("✅ The updated Senior Developer Agent now:")
    print("- Emphasizes following exact requirements")
    print("- Prevents adding imaginary features")
    print("- Focuses on implementing what was specifically requested")
    print("- Reviews implementations against original requirements")
    print("- Saves code that matches the exact specifications")

if __name__ == "__main__":
    asyncio.run(test_exact_instructions()) 