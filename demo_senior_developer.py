#!/usr/bin/env python3
"""
Demonstration of the Senior Developer Agent functionality
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
from src.github_mcp_client import GitHubMCPClient, GitHubIssue

# Load environment variables
load_dotenv()

async def demo_senior_developer():
    """Demonstrate the Senior Developer Agent functionality"""
    
    print("🤖 Senior Developer Agent - Demonstration")
    print("=" * 60)
    print("This demo shows how the Senior Developer Agent works:")
    print("1. Reads AI tasks labeled as 'ai-task' from GitHub")
    print("2. Analyzes task requirements and comments")
    print("3. Implements solutions with clean, documented code")
    print("4. Reviews code for quality and best practices")
    print("5. Saves implementations to files")
    print()
    
    # Mock AI tasks for demonstration
    mock_ai_tasks = [
        GitHubIssue(
            number=123,
            title="Implement sentiment analysis API",
            body="""Create a REST API endpoint that performs sentiment analysis on text input.
            
Requirements:
- Accept POST requests with JSON payload containing 'text' field
- Use a pre-trained model for sentiment analysis
- Return sentiment score (0-1) and label (positive/negative/neutral)
- Include proper error handling and validation
- Add comprehensive documentation

Example request:
{
  "text": "I love this product!"
}

Example response:
{
  "sentiment": "positive",
  "score": 0.85,
  "confidence": 0.92
}""",
            state="open",
            labels=[{"name": "ai-task"}, {"name": "api"}],
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
            html_url="https://github.com/test/repo/issues/123"
        ),
        GitHubIssue(
            number=124,
            title="Create machine learning data preprocessing pipeline",
            body="""Build a data preprocessing pipeline for machine learning projects.

Requirements:
- Handle missing values and outliers
- Feature scaling and normalization
- Categorical variable encoding
- Data validation and quality checks
- Support for multiple data formats (CSV, JSON, Excel)
- Configurable preprocessing steps
- Unit tests for all functions

The pipeline should be modular and reusable across different ML projects.""",
            state="open",
            labels=[{"name": "ai-task"}, {"name": "ml"}],
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
            html_url="https://github.com/test/repo/issues/124"
        )
    ]
    
    print("📋 Mock AI Tasks Found:")
    for task in mock_ai_tasks:
        print(f"  • #{task.number}: {task.title}")
        print(f"    Labels: {', '.join([label['name'] for label in task.labels])}")
        print(f"    State: {task.state}")
        print()
    
    print("🤖 Senior Developer Agent Process:")
    print("1. Task Reader Agent: Analyzes requirements and objectives")
    print("2. Senior Developer Agent: Implements solutions with clean code")
    print("3. Code Reviewer Agent: Reviews quality and best practices")
    print()
    
    print("💻 Expected Output:")
    print("- Complete code implementations")
    print("- Documentation and usage instructions")
    print("- Testing approach")
    print("- Code quality assessment")
    print("- Security and performance review")
    print("- Saved implementation files")
    print()
    
    print("🎯 To use with real GitHub repository:")
    print("1. Create issues labeled as 'ai-task'")
    print("2. Add detailed requirements in the issue description")
    print("3. Run: python main.py")
    print("4. Choose option 2 (Handle AI tasks)")
    print("5. The agent will automatically process all 'ai-task' issues")
    print()
    
    print("📁 Generated files will be saved to:")
    print("   ai_task_implementations/")
    print("   - ai_task_implementation_1.py")
    print("   - ai_task_implementation_2.py")
    print("   - etc...")
    print()
    
    print("✅ Senior Developer Agent is ready to handle AI tasks!")
    print("The agent can work with any programming language and framework.")
    print("It provides production-ready code with proper documentation.")

if __name__ == "__main__":
    asyncio.run(demo_senior_developer()) 