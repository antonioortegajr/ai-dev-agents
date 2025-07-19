import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
import aiohttp
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class GitHubIssue(BaseModel):
    """Model for GitHub issue data"""
    number: int
    title: str
    body: str
    state: str
    labels: List[Dict[str, Any]]
    created_at: str
    updated_at: str
    html_url: str

class GitHubMCPClient:
    """Client for interacting with GitHub MCP server"""
    
    def __init__(self, server_url: str = "http://localhost:3000"):
        self.server_url = server_url
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_issues_by_label(self, repository: str, label: str) -> List[GitHubIssue]:
        """
        Get issues from a repository filtered by a specific label
        
        Args:
            repository: Repository in format 'owner/repo'
            label: Label to filter by
            
        Returns:
            List of GitHubIssue objects
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # MCP call to get issues with specific label
            payload = {
                "method": "github.list_issues",
                "params": {
                    "owner": repository.split('/')[0],
                    "repo": repository.split('/')[1],
                    "labels": [label],
                    "state": "all"  # Get both open and closed issues
                }
            }
            
            async with self.session.post(
                f"{self.server_url}/call",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    issues = []
                    
                    if "result" in data and "issues" in data["result"]:
                        for issue_data in data["result"]["issues"]:
                            try:
                                issue = GitHubIssue(**issue_data)
                                issues.append(issue)
                            except Exception as e:
                                logger.warning(f"Failed to parse issue {issue_data.get('number', 'unknown')}: {e}")
                    
                    return issues
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to get issues: {response.status} - {error_text}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting issues by label: {e}")
            return []
    
    async def get_all_open_issues(self, repository: str) -> List[GitHubIssue]:
        """
        Get all open issues from a repository (regardless of labels)
        
        Args:
            repository: Repository in format 'owner/repo'
            
        Returns:
            List of GitHubIssue objects
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # MCP call to get all open issues
            payload = {
                "method": "github.list_issues",
                "params": {
                    "owner": repository.split('/')[0],
                    "repo": repository.split('/')[1],
                    "state": "open"  # Get only open issues
                }
            }
            
            async with self.session.post(
                f"{self.server_url}/call",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    issues = []
                    
                    if "result" in data and "issues" in data["result"]:
                        for issue_data in data["result"]["issues"]:
                            try:
                                issue = GitHubIssue(**issue_data)
                                issues.append(issue)
                            except Exception as e:
                                logger.warning(f"Failed to parse issue {issue_data.get('number', 'unknown')}: {e}")
                    
                    return issues
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to get all open issues: {response.status} - {error_text}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting all open issues: {e}")
            return []
    
    async def get_issue_details(self, repository: str, issue_number: int) -> Optional[GitHubIssue]:
        """
        Get detailed information about a specific issue
        
        Args:
            repository: Repository in format 'owner/repo'
            issue_number: Issue number to retrieve
            
        Returns:
            GitHubIssue object or None if not found
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            payload = {
                "method": "github.get_issue",
                "params": {
                    "owner": repository.split('/')[0],
                    "repo": repository.split('/')[1],
                    "issue_number": issue_number
                }
            }
            
            async with self.session.post(
                f"{self.server_url}/call",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if "result" in data and "issue" in data["result"]:
                        return GitHubIssue(**data["result"]["issue"])
                    else:
                        logger.warning(f"No issue data found for #{issue_number}")
                        return None
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to get issue #{issue_number}: {response.status} - {error_text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting issue details: {e}")
            return None
    
    async def close_issue(self, repository: str, issue_number: int, comment: str = None) -> bool:
        """
        Close an issue with an optional comment
        
        Args:
            repository: Repository in format 'owner/repo'
            issue_number: Issue number to close
            comment: Optional comment to add when closing
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            payload = {
                "method": "github.close_issue",
                "params": {
                    "owner": repository.split('/')[0],
                    "repo": repository.split('/')[1],
                    "issue_number": issue_number,
                    "comment": comment
                }
            }
            
            async with self.session.post(
                f"{self.server_url}/call",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    success = data.get("result", {}).get("success", False)
                    if success:
                        logger.info(f"Successfully closed issue #{issue_number}")
                    else:
                        logger.error(f"Failed to close issue #{issue_number}")
                    return success
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to close issue #{issue_number}: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error closing issue: {e}")
            return False
    
    async def add_issue_comment(self, repository: str, issue_number: int, comment: str) -> bool:
        """
        Add a comment to an issue
        
        Args:
            repository: Repository in format 'owner/repo'
            issue_number: Issue number to comment on
            comment: Comment text to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            payload = {
                "method": "github.add_issue_comment",
                "params": {
                    "owner": repository.split('/')[0],
                    "repo": repository.split('/')[1],
                    "issue_number": issue_number,
                    "comment": comment
                }
            }
            
            async with self.session.post(
                f"{self.server_url}/call",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    success = data.get("result", {}).get("success", False)
                    if success:
                        logger.info(f"Successfully added comment to issue #{issue_number}")
                    else:
                        logger.error(f"Failed to add comment to issue #{issue_number}")
                    return success
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to add comment to issue #{issue_number}: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error adding comment: {e}")
            return False
    
    async def create_pull_request(self, repository: str, title: str, body: str, 
                                 head: str, base: str = "main") -> Optional[Dict[str, Any]]:
        """
        Create a pull request
        
        Args:
            repository: Repository in format 'owner/repo'
            title: Pull request title
            body: Pull request description
            head: Source branch name
            base: Target branch name (default: main)
            
        Returns:
            Pull request data or None if failed
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            payload = {
                "method": "github.create_pull_request",
                "params": {
                    "owner": repository.split('/')[0],
                    "repo": repository.split('/')[1],
                    "title": title,
                    "body": body,
                    "head": head,
                    "base": base
                }
            }
            
            async with self.session.post(
                f"{self.server_url}/call",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    pr_data = data.get("result", {}).get("pull_request")
                    if pr_data:
                        logger.info(f"Successfully created pull request #{pr_data.get('number', 'unknown')}")
                    else:
                        logger.error("Failed to create pull request")
                    return pr_data
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to create pull request: {response.status} - {error_text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error creating pull request: {e}")
            return None
    
    async def create_branch(self, repository: str, branch_name: str, base_branch: str = "main") -> bool:
        """
        Create a new branch in the repository
        
        Args:
            repository: Repository in format 'owner/repo'
            branch_name: Name of the new branch
            base_branch: Base branch to create from (default: main)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            payload = {
                "method": "github.create_branch",
                "params": {
                    "owner": repository.split('/')[0],
                    "repo": repository.split('/')[1],
                    "branch_name": branch_name,
                    "base_branch": base_branch
                }
            }
            
            async with self.session.post(
                f"{self.server_url}/call",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    success = data.get("result", {}).get("success", False)
                    if success:
                        logger.info(f"Successfully created branch {branch_name}")
                    else:
                        logger.error(f"Failed to create branch {branch_name}")
                    return success
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to create branch {branch_name}: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error creating branch: {e}")
            return False
    
    async def create_file(self, repository: str, path: str, content: str, 
                         branch: str, message: str) -> bool:
        """
        Create a file in the repository
        
        Args:
            repository: Repository in format 'owner/repo'
            path: File path in the repository
            content: File content
            branch: Branch to create the file in
            message: Commit message
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            payload = {
                "method": "github.create_file",
                "params": {
                    "owner": repository.split('/')[0],
                    "repo": repository.split('/')[1],
                    "path": path,
                    "content": content,
                    "branch": branch,
                    "message": message
                }
            }
            
            async with self.session.post(
                f"{self.server_url}/call",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    success = data.get("result", {}).get("success", False)
                    if success:
                        logger.info(f"Successfully created file {path}")
                    else:
                        logger.error(f"Failed to create file {path}")
                    return success
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to create file {path}: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error creating file: {e}")
            return False 