import asyncio
import json
import logging
import os
from typing import Dict, Any, List, Optional
from aiohttp import web, ClientSession
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class MCPRequest(BaseModel):
    method: str
    params: Dict[str, Any]

class MCPResponse(BaseModel):
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class GitHubMCPServer:
    """Simple MCP server for GitHub operations"""
    
    def __init__(self, github_token: str):
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        self.session: Optional[ClientSession] = None
    
    async def __aenter__(self):
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-MCP-Server"
        }
        self.session = ClientSession(headers=headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def list_issues(self, owner: str, repo: str, labels: List[str] = None, state: str = "all") -> List[Dict[str, Any]]:
        """List issues from a GitHub repository"""
        try:
            if not self.session or self.session.closed:
                logger.error("Session is closed or not initialized")
                return []
            
            url = f"{self.base_url}/repos/{owner}/{repo}/issues"
            params = {"state": state}
            
            if labels:
                params["labels"] = ",".join(labels)
            
            logger.info(f"Making request to: {url} with params: {params}")
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    issues = await response.json()
                    logger.info(f"Successfully retrieved {len(issues)} issues")
                    return issues
                else:
                    error_text = await response.text()
                    logger.error(f"GitHub API error: {response.status} - {error_text}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error listing issues: {e}")
            return []
    
    async def get_issue(self, owner: str, repo: str, issue_number: int) -> Optional[Dict[str, Any]]:
        """Get a specific issue from a GitHub repository"""
        try:
            if not self.session or self.session.closed:
                logger.error("Session is closed or not initialized")
                return None
            
            url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}"
            
            logger.info(f"Making request to: {url}")
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    issue = await response.json()
                    logger.info(f"Successfully retrieved issue #{issue_number}")
                    return issue
                else:
                    error_text = await response.text()
                    logger.error(f"GitHub API error: {response.status} - {error_text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting issue: {e}")
            return None
    
    async def close_issue(self, owner: str, repo: str, issue_number: int, comment: str = None) -> bool:
        """Close an issue with an optional comment"""
        try:
            if not self.session or self.session.closed:
                logger.error("Session is closed or not initialized")
                return False
            
            url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}"
            
            # Prepare the update data
            update_data = {"state": "closed"}
            
            logger.info(f"Closing issue #{issue_number} in {owner}/{repo}")
            
            async with self.session.patch(url, json=update_data) as response:
                if response.status == 200:
                    logger.info(f"Successfully closed issue #{issue_number}")
                    
                    # Add a comment if provided
                    if comment:
                        await self.add_issue_comment(owner, repo, issue_number, comment)
                    
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f"GitHub API error: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error closing issue: {e}")
            return False
    
    async def add_issue_comment(self, owner: str, repo: str, issue_number: int, comment: str) -> bool:
        """Add a comment to an issue"""
        try:
            if not self.session or self.session.closed:
                logger.error("Session is closed or not initialized")
                return False
            
            url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
            
            logger.info(f"Adding comment to issue #{issue_number}")
            
            async with self.session.post(url, json={"body": comment}) as response:
                if response.status == 201:
                    logger.info(f"Successfully added comment to issue #{issue_number}")
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f"GitHub API error: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error adding comment: {e}")
            return False
    
    async def create_pull_request(self, owner: str, repo: str, title: str, body: str, 
                                 head: str, base: str = "main") -> Optional[Dict[str, Any]]:
        """Create a pull request"""
        try:
            if not self.session or self.session.closed:
                logger.error("Session is closed or not initialized")
                return None
            
            url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
            
            pr_data = {
                "title": title,
                "body": body,
                "head": head,
                "base": base
            }
            
            logger.info(f"Creating pull request in {owner}/{repo}")
            
            async with self.session.post(url, json=pr_data) as response:
                if response.status == 201:
                    pr = await response.json()
                    logger.info(f"Successfully created pull request #{pr['number']}")
                    return pr
                else:
                    error_text = await response.text()
                    logger.error(f"GitHub API error: {response.status} - {error_text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error creating pull request: {e}")
            return None
    
    async def create_branch(self, owner: str, repo: str, branch_name: str, base_branch: str = "main") -> bool:
        """Create a new branch from the base branch"""
        try:
            if not self.session or self.session.closed:
                logger.error("Session is closed or not initialized")
                return False
            
            # First, get the SHA of the base branch
            ref_url = f"{self.base_url}/repos/{owner}/{repo}/git/ref/heads/{base_branch}"
            
            async with self.session.get(ref_url) as response:
                if response.status == 200:
                    ref_data = await response.json()
                    sha = ref_data['object']['sha']
                    
                    # Create the new branch
                    create_url = f"{self.base_url}/repos/{owner}/{repo}/git/refs"
                    branch_data = {
                        "ref": f"refs/heads/{branch_name}",
                        "sha": sha
                    }
                    
                    async with self.session.post(create_url, json=branch_data) as create_response:
                        if create_response.status == 201:
                            logger.info(f"Successfully created branch {branch_name}")
                            return True
                        else:
                            error_text = await create_response.text()
                            logger.error(f"GitHub API error creating branch: {create_response.status} - {error_text}")
                            return False
                else:
                    error_text = await response.text()
                    logger.error(f"GitHub API error getting base branch: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error creating branch: {e}")
            return False
    
    async def create_file(self, owner: str, repo: str, path: str, content: str, 
                         branch: str, message: str) -> bool:
        """Create a file in the repository"""
        try:
            if not self.session or self.session.closed:
                logger.error("Session is closed or not initialized")
                return False
            
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
            
            file_data = {
                "message": message,
                "content": content,
                "branch": branch
            }
            
            logger.info(f"Creating file {path} in {owner}/{repo}")
            
            async with self.session.put(url, json=file_data) as response:
                if response.status == 201:
                    logger.info(f"Successfully created file {path}")
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f"GitHub API error: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error creating file: {e}")
            return False

class MCPHandler:
    """Handler for MCP server requests"""
    
    def __init__(self, github_server: GitHubMCPServer):
        self.github_server = github_server
    
    async def handle_call(self, request: web.Request) -> web.Response:
        """Handle MCP call requests"""
        try:
            data = await request.json()
            mcp_request = MCPRequest(**data)
            
            if mcp_request.method == "github.list_issues":
                result = await self.github_server.list_issues(
                    owner=mcp_request.params["owner"],
                    repo=mcp_request.params["repo"],
                    labels=mcp_request.params.get("labels", []),
                    state=mcp_request.params.get("state", "all")
                )
                
                response = MCPResponse(result={"issues": result})
                
            elif mcp_request.method == "github.get_issue":
                result = await self.github_server.get_issue(
                    owner=mcp_request.params["owner"],
                    repo=mcp_request.params["repo"],
                    issue_number=mcp_request.params["issue_number"]
                )
                
                response = MCPResponse(result={"issue": result})
                
            elif mcp_request.method == "github.close_issue":
                result = await self.github_server.close_issue(
                    owner=mcp_request.params["owner"],
                    repo=mcp_request.params["repo"],
                    issue_number=mcp_request.params["issue_number"],
                    comment=mcp_request.params.get("comment")
                )
                
                response = MCPResponse(result={"success": result})
                
            elif mcp_request.method == "github.add_issue_comment":
                result = await self.github_server.add_issue_comment(
                    owner=mcp_request.params["owner"],
                    repo=mcp_request.params["repo"],
                    issue_number=mcp_request.params["issue_number"],
                    comment=mcp_request.params["comment"]
                )
                
                response = MCPResponse(result={"success": result})
                
            elif mcp_request.method == "github.create_pull_request":
                result = await self.github_server.create_pull_request(
                    owner=mcp_request.params["owner"],
                    repo=mcp_request.params["repo"],
                    title=mcp_request.params["title"],
                    body=mcp_request.params["body"],
                    head=mcp_request.params["head"],
                    base=mcp_request.params.get("base", "main")
                )
                
                response = MCPResponse(result={"pull_request": result})
                
            elif mcp_request.method == "github.create_branch":
                result = await self.github_server.create_branch(
                    owner=mcp_request.params["owner"],
                    repo=mcp_request.params["repo"],
                    branch_name=mcp_request.params["branch_name"],
                    base_branch=mcp_request.params.get("base_branch", "main")
                )
                
                response = MCPResponse(result={"success": result})
                
            elif mcp_request.method == "github.create_file":
                result = await self.github_server.create_file(
                    owner=mcp_request.params["owner"],
                    repo=mcp_request.params["repo"],
                    path=mcp_request.params["path"],
                    content=mcp_request.params["content"],
                    branch=mcp_request.params["branch"],
                    message=mcp_request.params["message"]
                )
                
                response = MCPResponse(result={"success": result})
                
            else:
                response = MCPResponse(error=f"Unknown method: {mcp_request.method}")
            
            return web.json_response(response.dict())
            
        except Exception as e:
            logger.error(f"Error handling MCP call: {e}")
            response = MCPResponse(error=str(e))
            return web.json_response(response.dict(), status=500)

async def create_mcp_server(github_token: str, host: str = "localhost", port: int = 3000):
    """Create and start the MCP server"""
    app = web.Application()
    
    # Create GitHub server without context manager to keep session alive
    github_server = GitHubMCPServer(github_token)
    await github_server.__aenter__()  # Initialize the session
    
    handler = MCPHandler(github_server)
    app["handler"] = handler
    app["github_server"] = github_server  # Store for cleanup
    
    app.router.add_post("/call", lambda req: app["handler"].handle_call(req))
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, host, port)
    await site.start()
    
    logger.info(f"MCP Server running on http://{host}:{port}")
    
    return runner, github_server

async def main():
    """Main function to run the MCP server"""
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        logger.error("GITHUB_TOKEN environment variable is required")
        return
    
    host = os.getenv("MCP_SERVER_HOST", "localhost")
    port = int(os.getenv("MCP_SERVER_PORT", "3000"))
    
    runner, github_server = await create_mcp_server(github_token, host, port)
    
    try:
        # Keep the server running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down MCP server...")
    finally:
        # Clean up resources
        await runner.cleanup()
        await github_server.__aexit__(None, None, None)  # Close the session

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main()) 