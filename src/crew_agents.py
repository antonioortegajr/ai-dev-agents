import asyncio
import logging
import json
import re
from typing import List, Dict, Any, Optional
from crewai import Agent, Task, Crew
from pydantic import BaseModel, Field

from .github_mcp_client import GitHubMCPClient, GitHubIssue

logger = logging.getLogger(__name__)

class GitHubIssueAgent:
    """Crew AI agent for reading and analyzing GitHub issues"""
    
    def __init__(self, mcp_client: GitHubMCPClient, llm_model: str = "gpt-4"):
        self.mcp_client = mcp_client
        self.llm_model = llm_model
    
    async def analyze_issues_by_label(self, repository: str, label: str) -> str:
        """
        Analyze issues from a repository filtered by a specific label
        
        Args:
            repository: Repository in format 'owner/repo'
            label: Label to filter by
            
        Returns:
            Analysis results as a string
        """
        try:
            # First, get the issues data
            issues = await self.mcp_client.get_issues_by_label(repository, label)
            all_open_issues = await self.mcp_client.get_all_open_issues(repository)
            
            if not issues:
                return f"No issues found with label '{label}' in repository '{repository}'"
            
            # Format the issues data with total counts
            issues_data = f"Repository Overview: {repository}\n"
            issues_data += f"Total open issues: {len(all_open_issues)}\n"
            issues_data += f"Issues with label '{label}': {len(issues)}\n"
            issues_data += f"Percentage of open issues with this label: {(len(issues) / len(all_open_issues) * 100):.1f}%\n\n"
            issues_data += f"Detailed issues with label '{label}':\n\n"
            
            for issue in issues:
                labels_str = ", ".join([label.get("name", "") for label in issue.labels])
                issues_data += f"Issue #{issue.number}: {issue.title}\n"
                issues_data += f"State: {issue.state}\n"
                issues_data += f"Labels: {labels_str}\n"
                issues_data += f"Created: {issue.created_at}\n"
                issues_data += f"Updated: {issue.updated_at}\n"
                issues_data += f"URL: {issue.html_url}\n"
                issues_data += f"Body: {issue.body[:200]}{'...' if len(issue.body) > 200 else ''}\n"
                issues_data += "-" * 50 + "\n"
            
            # Create agents for analysis
            issue_reader_agent = Agent(
                role="GitHub Issue Reader",
                goal="Read and collect GitHub issues from repositories filtered by labels",
                backstory="""You are an expert at reading and understanding GitHub issues. 
                You can efficiently collect issues from repositories and filter them by labels.
                You provide clear, organized summaries of issue data.""",
                verbose=True,
                allow_delegation=False,
                llm_model=self.llm_model
            )
            
            issue_analyst_agent = Agent(
                role="Issue Analyst",
                goal="Analyze GitHub issues to provide insights and recommendations",
                backstory="""You are an expert analyst who can examine GitHub issues and provide 
                valuable insights about patterns, trends, and recommendations for issue management.
                You help teams understand their issue landscape and suggest improvements.""",
                verbose=True,
                allow_delegation=False,
                llm_model=self.llm_model
            )
            
            # Create tasks
            read_task = Task(
                description=f"""Analyze the following GitHub issues data and provide a comprehensive summary:

{issues_data}

Provide a detailed summary of the issues including their titles, states, labels, and key information.""",
                agent=issue_reader_agent,
                expected_output="A detailed summary of all issues with the specified label"
            )
            
            analyze_task = Task(
                description=f"""Based on the issues data provided, create insights about:
                1. Issue distribution (open vs closed)
                2. Common patterns in labels
                3. Potential bottlenecks or areas of concern
                4. Recommendations for issue management
                
                Provide actionable insights and suggestions for the team.""",
                agent=issue_analyst_agent,
                expected_output="Comprehensive analysis with insights and recommendations",
                context=[read_task]
            )
            
            # Create crew
            crew = Crew(
                agents=[issue_reader_agent, issue_analyst_agent],
                tasks=[read_task, analyze_task],
                verbose=True
            )
            
            # Execute the crew
            result = crew.kickoff()
            return result
            
        except Exception as e:
            logger.error(f"Error in issue analysis: {e}")
            return f"Error analyzing issues: {str(e)}"


class SeniorDeveloperAgent:
    """Crew AI agent for handling AI tasks as a senior developer"""
    
    def __init__(self, mcp_client: GitHubMCPClient, llm_model: str = "gpt-4"):
        self.mcp_client = mcp_client
        self.llm_model = llm_model
    
    async def handle_ai_tasks(self, repository: str) -> str:
        """
        Handle AI tasks from a repository by reading tasks labeled as 'ai-task'
        
        Args:
            repository: Repository in format 'owner/repo'
            
        Returns:
            Task completion results as a string
        """
        try:
            # Get all issues with 'ai-task' label
            ai_tasks = await self.mcp_client.get_issues_by_label(repository, "ai-task")
            
            if not ai_tasks:
                return f"No AI tasks found in repository '{repository}'. Look for issues labeled as 'ai-task'."
            
            # Format the AI tasks data with emphasis on following exact instructions
            tasks_data = f"Repository: {repository}\n"
            tasks_data += f"Found {len(ai_tasks)} GitHub issues labeled as 'ai-task':\n\n"
            tasks_data += "IMPORTANT: These are REAL GitHub issues with specific requirements. "
            tasks_data += "You must follow the EXACT instructions provided in each issue.\n\n"
            
            for task in ai_tasks:
                tasks_data += f"ISSUE #{task.number}: {task.title}\n"
                tasks_data += f"State: {task.state}\n"
                tasks_data += f"URL: {task.html_url}\n"
                tasks_data += f"EXACT REQUIREMENTS:\n{task.body}\n"
                tasks_data += "-" * 50 + "\n"
            
            # Create agents for AI task handling
            task_reader_agent = Agent(
                role="AI Task Reader",
                goal="Read and understand the EXACT requirements from GitHub issues",
                backstory="""You are an expert at reading and understanding GitHub issues. Your job is to extract 
                the EXACT requirements, specifications, and instructions from each issue. You must follow the 
                instructions precisely as written in the issue description and comments. Do not make assumptions 
                or add requirements that are not explicitly stated in the issue.""",
                verbose=True,
                allow_delegation=False,
                llm_model=self.llm_model
            )
            
            senior_dev_agent = Agent(
                role="Senior Developer",
                goal="Implement solutions that EXACTLY follow the task instructions",
                backstory="""You are a senior software developer who implements solutions that follow the EXACT 
                specifications provided in GitHub issues. You must implement what is requested, no more, no less. 
                Follow the requirements precisely as stated in the issue description. Do not add features or 
                requirements that are not explicitly mentioned in the original task. You can use the MCP client to get the issues and the repository information.
                You can use the MCP client to open pull requests if an issues is asking for code changes. 
                You can use the MCP client to close invalid or completed issues.""",
                verbose=True,
                allow_delegation=False,
                llm_model=self.llm_model
            )
            
            code_reviewer_agent = Agent(
                role="Code Reviewer",
                goal="Verify that the implementation EXACTLY matches the task requirements",
                backstory="""You are an expert code reviewer who verifies that implementations EXACTLY match 
                the requirements stated in the GitHub issues. You check that the code follows the specifications 
                precisely and does not add unnecessary features or deviate from the original task description.""",
                verbose=True,
                allow_delegation=False,
                llm_model=self.llm_model
            )
            
            # Create tasks
            read_task = Task(
                description=f"""Carefully analyze the following GitHub issues labeled as 'ai-task'. Your job is to extract 
                the EXACT requirements and instructions from each issue:

{tasks_data}

IMPORTANT: You must follow the instructions EXACTLY as written in each issue. Do not:
- Add requirements that are not explicitly stated
- Make assumptions about what the user wants
- Suggest additional features not mentioned in the issue
- Deviate from the original task description

For each task, identify ONLY what is explicitly stated in the issue:
1. The exact objective as described in the issue
2. The specific technical requirements mentioned
3. The exact deliverables requested
4. Any constraints or dependencies explicitly stated
5. The priority level if mentioned in the issue

Provide a precise breakdown of what each issue specifically requests.""",
                agent=task_reader_agent,
                expected_output="Exact analysis of each task's requirements as stated in the GitHub issues"
            )
            
            implement_task = Task(
                description=f"""Based on the task analysis, implement solutions that EXACTLY follow the requirements 
                stated in the GitHub issues:

CRITICAL REQUIREMENTS:
- Implement ONLY what is explicitly requested in each issue
- Do not add features or requirements not mentioned in the original task
- Follow the specifications precisely as written
- If the issue asks for a specific function, implement that function exactly
- If the issue asks for a specific API endpoint, implement that endpoint exactly
- If the issue asks for a specific file structure, follow that structure exactly

For each task, provide:
- Complete code implementation that matches the exact requirements
- Documentation that explains how the implementation meets the stated requirements
- Usage examples that demonstrate the requested functionality
- Any additional files or configurations explicitly requested

IMPORTANT: Your implementation must be a direct response to what is asked for in the GitHub issue. 
Do not add extra features, optimizations, or improvements unless they are explicitly requested.""",
                agent=senior_dev_agent,
                expected_output="Exact implementations that match the requirements stated in the GitHub issues",
                context=[read_task]
            )
            
            review_task = Task(
                description=f"""Review the implemented solutions to verify they EXACTLY match the requirements 
                stated in the GitHub issues:

CRITICAL REVIEW CRITERIA:
1. Verify that the implementation matches the EXACT requirements from the issue
2. Check that no extra features were added that weren't requested
3. Ensure the code does exactly what the issue asked for
4. Validate that the implementation follows the specifications precisely
5. Confirm that the solution addresses the stated problem or request

For each solution, provide:
- Verification that the implementation matches the exact requirements
- Assessment of whether the code does what was specifically requested
- Identification of any deviations from the original task description
- Confirmation that the solution is a direct response to the GitHub issue

IMPORTANT: Your review should focus on whether the implementation follows the exact instructions 
from the GitHub issue, not on general code quality improvements unless specifically requested.""",
                agent=code_reviewer_agent,
                expected_output="Verification that implementations exactly match the GitHub issue requirements",
                context=[implement_task]
            )
            
            # Create crew
            crew = Crew(
                agents=[task_reader_agent, senior_dev_agent, code_reviewer_agent],
                tasks=[read_task, implement_task, review_task],
                verbose=True
            )
            
            # Execute the crew
            result = crew.kickoff()
            
            # Take action on the issues based on the analysis
            action_results = await self._take_action_on_issues(repository, ai_tasks, result)
            
            return f"{result}\n\n{action_results}"
            
        except Exception as e:
            logger.error(f"Error handling AI tasks: {e}")
            return f"Error handling AI tasks: {str(e)}"
    
    def extract_code_blocks(self, text: str) -> List[Dict[str, str]]:
        """
        Extract code blocks from markdown text
        
        Args:
            text: Markdown text containing code blocks
            
        Returns:
            List of dictionaries with language and code content
        """
        code_blocks = []
        # Pattern to match markdown code blocks
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        for match in matches:
            language = match[0] if match[0] else 'text'
            code = match[1].strip()
            code_blocks.append({
                'language': language,
                'code': code
            })
        
        return code_blocks
    
    def save_implementations(self, result: str, output_dir: str = "ai_task_implementations") -> str:
        """
        Save code implementations to files
        
        Args:
            result: The result string containing code blocks
            output_dir: Directory to save implementations
            
        Returns:
            Summary of saved files
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        code_blocks = self.extract_code_blocks(result)
        saved_files = []
        
        for i, block in enumerate(code_blocks):
            if block['language'] in ['python', 'js', 'javascript', 'typescript', 'java', 'cpp', 'c', 'go', 'rust']:
                # Determine file extension based on language
                ext_map = {
                    'python': '.py',
                    'js': '.js',
                    'javascript': '.js',
                    'typescript': '.ts',
                    'java': '.java',
                    'cpp': '.cpp',
                    'c': '.c',
                    'go': '.go',
                    'rust': '.rs'
                }
                
                ext = ext_map.get(block['language'], '.txt')
                filename = f"ai_task_implementation_{i+1}{ext}"
                filepath = os.path.join(output_dir, filename)
                
                try:
                    with open(filepath, 'w') as f:
                        f.write(block['code'])
                    saved_files.append(filepath)
                except Exception as e:
                    logger.error(f"Error saving file {filepath}: {e}")
        
        if saved_files:
            return f"Saved {len(saved_files)} implementation files to {output_dir}:\n" + "\n".join(saved_files)
        else:
            return "No code files were saved (no valid code blocks found)"
    
    async def _take_action_on_issues(self, repository: str, ai_tasks: List[GitHubIssue], analysis_result: str) -> str:
        """
        Take action on issues based on the analysis result
        
        Args:
            repository: Repository in format 'owner/repo'
            ai_tasks: List of AI tasks to process
            analysis_result: Result from the Crew AI analysis
            
        Returns:
            Summary of actions taken
        """
        action_summary = []
        action_summary.append("=" * 50)
        action_summary.append("ACTIONS TAKEN ON ISSUES")
        action_summary.append("=" * 50)
        
        for task in ai_tasks:
            action_summary.append(f"\nProcessing Issue #{task.number}: {task.title}")
            
            # Check if the issue requires code changes
            if self._requires_code_changes(task):
                # Create a pull request for code changes
                pr_result = await self._create_pull_request_for_issue(repository, task, analysis_result)
                action_summary.append(f"✅ {pr_result}")
                
                # Add a comment to the issue with the PR link
                if "Successfully created pull request" in pr_result:
                    pr_url = pr_result.split(": ")[-1] if ": " in pr_result else "Pull request created"
                    comment = f"🤖 AI Agent has created a pull request to address this issue: {pr_url}\n\nPlease review the implementation."
                else:
                    comment = f"🤖 AI Agent attempted to create a pull request but encountered an issue: {pr_result}"
                
                await self.mcp_client.add_issue_comment(repository, task.number, comment)
                action_summary.append(f"✅ Added comment to issue #{task.number}")
                
            elif self._is_invalid_issue(task):
                # Close invalid issues
                comment = f"🤖 AI Agent: This issue appears to be invalid or unclear. Closing as requested."
                await self.mcp_client.close_issue(repository, task.number, comment)
                action_summary.append(f"✅ Closed invalid issue #{task.number}")
                
            elif self._is_completed_issue(task):
                # Close completed issues
                comment = f"🤖 AI Agent: This issue has been completed. Closing as requested."
                await self.mcp_client.close_issue(repository, task.number, comment)
                action_summary.append(f"✅ Closed completed issue #{task.number}")
                
            else:
                # Add a comment with the analysis
                comment = f"🤖 AI Agent Analysis:\n\n{analysis_result[:500]}..."
                await self.mcp_client.add_issue_comment(repository, task.number, comment)
                action_summary.append(f"✅ Added analysis comment to issue #{task.number}")
        
        return "\n".join(action_summary)
    
    def _requires_code_changes(self, task: GitHubIssue) -> bool:
        """Check if an issue requires code changes"""
        code_keywords = [
            "implement", "create", "add", "fix", "update", "modify", "change",
            "function", "class", "method", "api", "endpoint", "file", "code",
            "script", "module", "library", "package", "component"
        ]
        
        task_text = f"{task.title} {task.body}".lower()
        return any(keyword in task_text for keyword in code_keywords)
    
    def _is_invalid_issue(self, task: GitHubIssue) -> bool:
        """Check if an issue is invalid or unclear"""
        invalid_keywords = [
            "invalid", "unclear", "not clear", "confusing", "wrong", "error",
            "duplicate", "spam", "test", "example", "sample"
        ]
        
        task_text = f"{task.title} {task.body}".lower()
        return any(keyword in task_text for keyword in invalid_keywords)
    
    def _is_completed_issue(self, task: GitHubIssue) -> bool:
        """Check if an issue is already completed"""
        completed_keywords = [
            "done", "completed", "finished", "resolved", "fixed", "closed",
            "implemented", "added", "created"
        ]
        
        task_text = f"{task.title} {task.body}".lower()
        return any(keyword in task_text for keyword in completed_keywords)
    
    async def _create_pull_request_for_issue(self, repository: str, task: GitHubIssue, analysis_result: str) -> str:
        """Create a pull request for a code change issue"""
        try:
            # Extract code blocks from the analysis
            code_blocks = self.extract_code_blocks(analysis_result)
            
            if not code_blocks:
                return "No code implementation found in analysis"
            
            # Create a branch name for this issue
            branch_name = f"ai-task-{task.number}-{task.title.lower().replace(' ', '-')[:30]}"
            branch_name = "".join(c for c in branch_name if c.isalnum() or c == '-')
            
            # Create pull request title and body
            pr_title = f"🤖 AI Agent: Implement {task.title}"
            pr_body = f"""## AI Agent Implementation

This pull request implements the requirements from Issue #{task.number}: {task.title}

### Changes Made:
{task.body}

### Implementation:
The AI agent has analyzed the requirements and provided the following implementation:

```python
{code_blocks[0]['code'] if code_blocks else 'Implementation details in analysis'}
```

### Files Created/Modified:
- Generated implementation files saved to `ai_task_implementations/`

### Review Notes:
- This implementation follows the exact requirements from the GitHub issue
- No extra features were added beyond what was requested
- Code has been reviewed for accuracy and completeness

---
*This PR was automatically generated by the AI Dev Agents system.*"""
            
            # Actually create the pull request by creating branch, files, and PR
            try:
                # Step 1: Create the branch
                branch_created = await self.mcp_client.create_branch(
                    repository=repository,
                    branch_name=branch_name,
                    base_branch="main"
                )
                
                if not branch_created:
                    return f"❌ Failed to create branch {branch_name} for issue #{task.number}"
                
                # Step 2: Create implementation files in the branch
                files_created = 0
                for i, block in enumerate(code_blocks):
                    if block['language'] in ['python', 'js', 'javascript', 'typescript', 'java', 'cpp', 'c', 'go', 'rust']:
                        # Determine file extension and path
                        ext_map = {
                            'python': '.py',
                            'js': '.js',
                            'javascript': '.js',
                            'typescript': '.ts',
                            'java': '.java',
                            'cpp': '.cpp',
                            'c': '.c',
                            'go': '.go',
                            'rust': '.rs'
                        }
                        
                        ext = ext_map.get(block['language'], '.txt')
                        filename = f"ai_task_implementation_{i+1}{ext}"
                        file_path = f"ai_task_implementations/{filename}"
                        
                        # Create the file in the repository
                        file_created = await self.mcp_client.create_file(
                            repository=repository,
                            path=file_path,
                            content=block['code'],
                            branch=branch_name,
                            message=f"Add implementation for issue #{task.number}"
                        )
                        
                        if file_created:
                            files_created += 1
                
                if files_created == 0:
                    return f"❌ No implementation files were created for issue #{task.number}"
                
                # Step 3: Create the pull request
                pr_result = await self.mcp_client.create_pull_request(
                    repository=repository,
                    title=pr_title,
                    body=pr_body,
                    head=branch_name,
                    base="main"
                )
                
                if pr_result:
                    pr_number = pr_result.get('number', 'unknown')
                    pr_url = pr_result.get('html_url', 'unknown')
                    return f"✅ Successfully created pull request #{pr_number}: {pr_url}"
                else:
                    return f"❌ Failed to create pull request for issue #{task.number}"
                
            except Exception as pr_error:
                logger.error(f"Error creating pull request: {pr_error}")
                return f"❌ Error creating pull request: {str(pr_error)}"
            
        except Exception as e:
            logger.error(f"Error creating pull request for issue #{task.number}: {e}")
            return f"Error creating pull request: {str(e)}" 