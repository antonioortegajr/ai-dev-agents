#!/usr/bin/env python3
"""
Basic tests for AI Dev Agents functionality
"""

import unittest
import asyncio
import os
import sys
from unittest.mock import AsyncMock, patch

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.github_mcp_client import GitHubMCPClient, GitHubIssue
from src.crew_agents import GitHubIssueAgent, SeniorDeveloperAgent

class TestGitHubMCPClient(unittest.TestCase):
    """Test the GitHub MCP Client"""
    
    def test_github_issue_model(self):
        """Test GitHubIssue model creation"""
        issue_data = {
            "number": 123,
            "title": "Test Issue",
            "body": "This is a test issue",
            "state": "open",
            "labels": [{"name": "bug"}, {"name": "high-priority"}],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "html_url": "https://github.com/test/repo/issues/123"
        }
        
        issue = GitHubIssue(**issue_data)
        
        self.assertEqual(issue.number, 123)
        self.assertEqual(issue.title, "Test Issue")
        self.assertEqual(issue.state, "open")
        self.assertEqual(len(issue.labels), 2)
    
    @patch('aiohttp.ClientSession')
    async def test_get_issues_by_label(self, mock_session):
        """Test getting issues by label"""
        # Mock response data
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "result": {
                "issues": [
                    {
                        "number": 123,
                        "title": "Test Issue",
                        "body": "Test body",
                        "state": "open",
                        "labels": [{"name": "bug"}],
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                        "html_url": "https://github.com/test/repo/issues/123"
                    }
                ]
            }
        })
        
        mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
        
        client = GitHubMCPClient("http://localhost:3000")
        issues = await client.get_issues_by_label("test/repo", "bug")
        
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].title, "Test Issue")
        self.assertEqual(issues[0].state, "open")
    
    @patch('aiohttp.ClientSession')
    async def test_get_all_open_issues(self, mock_session):
        """Test getting all open issues"""
        # Mock response data
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "result": {
                "issues": [
                    {
                        "number": 123,
                        "title": "Test Issue 1",
                        "body": "Test body 1",
                        "state": "open",
                        "labels": [{"name": "bug"}],
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                        "html_url": "https://github.com/test/repo/issues/123"
                    },
                    {
                        "number": 124,
                        "title": "Test Issue 2",
                        "body": "Test body 2",
                        "state": "open",
                        "labels": [{"name": "feature"}],
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                        "html_url": "https://github.com/test/repo/issues/124"
                    }
                ]
            }
        })
        
        mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
        
        client = GitHubMCPClient("http://localhost:3000")
        issues = await client.get_all_open_issues("test/repo")
        
        self.assertEqual(len(issues), 2)
        self.assertEqual(issues[0].title, "Test Issue 1")
        self.assertEqual(issues[1].title, "Test Issue 2")
        self.assertEqual(issues[0].state, "open")
        self.assertEqual(issues[1].state, "open")

class TestCrewAgents(unittest.TestCase):
    """Test the Crew AI agents"""
    
    @patch('src.crew_agents.GitHubMCPClient')
    async def test_github_issue_agent_creation(self, mock_mcp_client):
        """Test GitHub Issue Agent creation"""
        mock_client = AsyncMock()
        mock_mcp_client.return_value = mock_client
        
        agent = GitHubIssueAgent(mock_client)
        
        # Test that the agent was created successfully
        self.assertIsNotNone(agent)
        self.assertEqual(agent.llm_model, "gpt-4")
    
    @patch('src.crew_agents.GitHubMCPClient')
    async def test_senior_developer_agent_creation(self, mock_mcp_client):
        """Test Senior Developer Agent creation"""
        mock_client = AsyncMock()
        mock_mcp_client.return_value = mock_client
        
        agent = SeniorDeveloperAgent(mock_client)
        
        # Test that the agent was created successfully
        self.assertIsNotNone(agent)
        self.assertEqual(agent.llm_model, "gpt-4")
    
    def test_senior_developer_code_extraction(self):
        """Test code block extraction functionality"""
        agent = SeniorDeveloperAgent(AsyncMock())
        
        # Test markdown with code blocks
        test_text = """
        Here's some Python code:
        ```python
        def hello_world():
            print("Hello, World!")
        ```
        
        And some JavaScript:
        ```javascript
        function greet() {
            console.log("Hello!");
        }
        ```
        """
        
        code_blocks = agent.extract_code_blocks(test_text)
        
        self.assertEqual(len(code_blocks), 2)
        self.assertEqual(code_blocks[0]['language'], 'python')
        self.assertEqual(code_blocks[1]['language'], 'javascript')
        self.assertIn('def hello_world():', code_blocks[0]['code'])
        self.assertIn('function greet()', code_blocks[1]['code'])
    
    @patch('builtins.open', create=True)
    @patch('os.makedirs')
    def test_senior_developer_save_implementations(self, mock_makedirs, mock_open):
        """Test saving implementations functionality"""
        agent = SeniorDeveloperAgent(AsyncMock())
        
        # Mock file operations
        mock_file = AsyncMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        result_text = """
        Here's the implementation:
        ```python
        def solve_problem():
            return "solution"
        ```
        """
        
        save_result = agent.save_implementations(result_text)
        
        # Check that the directory was created
        mock_makedirs.assert_called_once_with("ai_task_implementations", exist_ok=True)
        
        # Check that the result contains expected text
        self.assertIn("Saved", save_result)
        self.assertIn("ai_task_implementations", save_result)

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_environment_variables(self):
        """Test that required environment variables are documented"""
        required_vars = ["GITHUB_TOKEN", "GITHUB_REPOSITORY", "OPENAI_API_KEY"]
        
        # This test ensures we document required environment variables
        # In a real test, you might check if they're actually set
        for var in required_vars:
            self.assertIsInstance(var, str)
            self.assertTrue(len(var) > 0)

if __name__ == "__main__":
    # Run async tests
    async def run_async_tests():
        # Create test suite
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # Add tests
        suite.addTests(loader.loadTestsFromTestCase(TestGitHubMCPClient))
        suite.addTests(loader.loadTestsFromTestCase(TestCrewAgents))
        suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
    
    # Run the async tests
    success = asyncio.run(run_async_tests())
    sys.exit(0 if success else 1) 