# AI Dev Agents

A powerful AI-driven development assistant that uses Crew AI and GitHub MCP (Model Context Protocol) server to read and analyze GitHub issues filtered by labels, and includes a senior developer agent that can handle AI tasks.

## Features

- 🤖 **Crew AI Integration**: Multi-agent system for intelligent issue analysis
- 📊 **GitHub Issue Analysis**: Read and analyze issues filtered by labels
- 🔧 **MCP Server**: Custom GitHub MCP server for seamless API integration
- 📈 **Smart Insights**: Automated analysis with recommendations and patterns
- 🏷️ **Label-based Filtering**: Filter issues by specific labels with total issue counts
- 👨‍💻 **Senior Developer Agent**: AI agent that follows EXACT instructions from GitHub issues
- 💻 **Precise Code Generation**: Implements only what is specifically requested in the issue
- 📁 **File Management**: Save generated code implementations to files
- 🎯 **Exact Requirements**: No imaginary features or assumptions - only what's explicitly stated
- 🔄 **Action Taking**: Closes issues and creates pull requests via GitHub API
- 💬 **Issue Management**: Adds comments and manages issue lifecycle

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Crew AI       │    │   GitHub MCP    │    │   GitHub API    │
│   Agents        │◄──►│   Server        │◄──►│   (Issues)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: This project uses Crew AI 0.1.32 which is compatible with Python 3.9+. If you encounter any issues, make sure you're using Python 3.9 or higher.

### 2. Set Up Environment Variables

Copy the example environment file and configure your settings:

```bash
cp env.example .env
```

Edit `.env` with your configuration:

```env
# GitHub API Configuration
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_REPOSITORY=owner/repository_name

# Crew AI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# MCP Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=3000
```

### 3. Start the MCP Server

```bash
python main.py server
```

### 4. Run the Application

```bash
python main.py
```

## Usage

### Running the MCP Server

The MCP server provides a REST API interface to GitHub operations:

```bash
# Start the server
python main.py server

# Or run directly
python src/mcp_server.py
```

The server will be available at `http://localhost:3000`

### Running the Main Application

```bash
python main.py
```

### Running the Demo

```bash
python demo_senior_developer.py
```

The application will:
1. Connect to the MCP server
2. Choose operation mode (issue analysis or AI task handling)
3. For issue analysis: Prompt for a label to filter by
4. For AI tasks: Look for issues labeled as "ai-task"
5. Fetch issues from the specified repository (both filtered and total open issues)
6. Display repository statistics and percentages
7. Use Crew AI agents to analyze the issues or handle AI tasks
8. Provide insights and recommendations or generate code implementations

### Example Output

#### Issue Analysis Mode
```
🤖 AI Dev Agents - GitHub Issue Analysis
==================================================
Repository: owner/repo
MCP Server: http://localhost:3000

Choose operation mode:
1. Analyze issues by label
2. Handle AI tasks (senior developer)

Enter your choice (1 or 2): 1

Enter the label to filter issues by: bug

Analyzing issues with label 'bug' in owner/repo...

Testing MCP server connection...
📊 Repository Statistics:
   Total open issues: 25
   Issues with label 'bug': 5
   Percentage: 20.0%

Starting Crew AI analysis...

==================================================
ANALYSIS RESULTS
==================================================
Analysis of 5 issues:

Open issues: 3
Closed issues: 2

Open Issues Summary:
- Fix login authentication bug
- Resolve database connection timeout
- Update user profile validation

Most common labels:
- bug: 5 issues
- high-priority: 2 issues
- frontend: 2 issues

Recommendations:
- Consider prioritizing open issues for resolution
- Consider implementing issue templates for better organization
```

#### Senior Developer Mode
```
🤖 Senior Developer Agent - Handling AI Tasks
==================================================
Repository: owner/repo
Looking for issues labeled as 'ai-task'...

Testing MCP server connection...
Starting Senior Developer analysis...

==================================================
AI TASK HANDLING RESULTS
==================================================
Task Analysis:
- Issue #123: Create a simple calculator function (exact requirements followed)
- Issue #124: Implement user authentication API (specific endpoints only)

Implementation:
```python
# calculator.py - EXACTLY as requested in the issue
def calculate(num1, num2, operator):
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        if num2 == 0:
            raise ValueError("Division by zero")
        return num1 / num2
    else:
        raise ValueError("Invalid operator")
```

Code Review:
- ✅ Matches exact requirements from GitHub issue
- ✅ Function name is exactly 'calculate' as requested
- ✅ Handles division by zero as specified
- ✅ No extra features added
- ✅ File name matches requirement

==================================================
SAVING IMPLEMENTATIONS
==================================================
Saved 2 implementation files to ai_task_implementations:
ai_task_implementations/ai_task_implementation_1.py
ai_task_implementations/ai_task_implementation_2.py

==================================================
ACTIONS TAKEN ON ISSUES
==================================================
Processing Issue #123: Create a simple calculator function
✅ Successfully created pull request #15: https://github.com/owner/repo/pull/15
✅ Added comment to issue #123

Processing Issue #124: Invalid test issue
✅ Closed invalid issue #124
```

## API Endpoints

### MCP Server Endpoints

- `POST /call` - Execute MCP methods

#### Available Methods

- `github.list_issues` - List issues with optional filtering
- `github.get_issue` - Get specific issue details
- `github.close_issue` - Close issues with optional comments
- `github.add_issue_comment` - Add comments to issues
- `github.create_pull_request` - Create pull requests for code changes
- `github.create_branch` - Create new branches for PRs
- `github.create_file` - Create files in repository branches

## Crew AI Agents

### Issue Analysis Agents

#### Issue Reader Agent
- **Role**: GitHub Issue Reader
- **Goal**: Read and collect GitHub issues from repositories filtered by labels
- **Functionality**: Analyzes and summarizes issue data

#### Issue Analyst Agent
- **Role**: Issue Analyst
- **Goal**: Analyze GitHub issues to provide insights and recommendations
- **Functionality**: Provides actionable insights and suggestions

### Senior Developer Agents

#### AI Task Reader Agent
- **Role**: AI Task Reader
- **Goal**: Read and understand AI tasks from GitHub issues
- **Functionality**: Analyzes task descriptions, requirements, and comments

#### Senior Developer Agent
- **Role**: Senior Developer
- **Goal**: Implement solutions that EXACTLY follow the task instructions from GitHub issues
- **Functionality**: Writes code that matches the exact specifications, no more, no less

#### Code Reviewer Agent
- **Role**: Code Reviewer
- **Goal**: Verify that the implementation EXACTLY matches the task requirements
- **Functionality**: Ensures the code follows the exact specifications from the GitHub issue

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub Personal Access Token | Yes |
| `GITHUB_REPOSITORY` | Repository in format `owner/repo` | Yes |
| `OPENAI_API_KEY` | OpenAI API Key for Crew AI | Yes |
| `MCP_SERVER_HOST` | MCP Server host (default: localhost) | No |
| `MCP_SERVER_PORT` | MCP Server port (default: 3000) | No |

### GitHub Token Setup

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` scope
3. Add the token to your `.env` file

## Development

### Project Structure

```
ai-dev-agents/
├── src/
│   ├── __init__.py
│   ├── github_mcp_client.py    # GitHub MCP client
│   ├── crew_agents.py          # Crew AI agents
│   └── mcp_server.py           # MCP server implementation
├── examples/
│   └── basic_usage.py          # Usage example
├── tests/
│   └── test_basic_functionality.py  # Basic tests
├── main.py                     # Main application
├── demo_senior_developer.py    # Senior developer agent demo
├── test_crew_fix.py           # Crew AI fix verification test
├── test_exact_instructions.py # Exact instructions following test
├── test_action_taking.py     # Action taking functionality test
├── test_real_pr_creation.py  # Real pull request creation test
├── start.sh                    # Startup script
├── requirements.txt            # Python dependencies
├── env.example                # Environment variables template
├── setup.py                   # Package setup
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

### Adding New Features

1. **New MCP Methods**: Add to `src/mcp_server.py`
2. **New Agents**: Extend the `GitHubIssueAgent` or `SeniorDeveloperAgent` classes
3. **New Analysis**: Modify the agent tasks in `src/crew_agents.py`
4. **New Task Types**: Add new task handlers to the `SeniorDeveloperAgent` class
5. **New Actions**: Add new action methods to handle different issue types

## Troubleshooting

### Common Issues

1. **Crew AI Import Errors**
   - Ensure you're using Python 3.9 or higher
   - Try reinstalling: `pip install crewai==0.1.32 --force-reinstall`

2. **MCP Server Connection Error**
   - Ensure the server is running: `python main.py server`
   - Check the server URL in your configuration

3. **GitHub API Errors**
   - Verify your GitHub token has the correct permissions
   - Check the repository name format (`owner/repo`)

4. **OpenAI API Errors**
   - Ensure your OpenAI API key is valid
   - Check your API key has sufficient credits

5. **MCP Server "Session is closed" Error**
   - Ensure the MCP server is running: `python main.py server`
   - Check that GITHUB_TOKEN is set correctly
   - Verify the server is accessible at http://localhost:3000
   - Test with: `python test_mcp_server.py`

6. **Crew AI "await" Error**
   - This has been fixed in the current version
   - The `crew.kickoff()` method is now called synchronously
   - Test with: `python test_crew_fix.py`

### Debug Mode

Enable debug logging by modifying the logging level in `main.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

### Warning Suppression

The application automatically suppresses common warnings:
- SSL compatibility warnings from urllib3
- Pydantic V1/V2 model mixing warnings
- Deprecation warnings

If you need to see all warnings, you can modify `src/warning_suppression.py` or set `suppress_warnings_flag=False` in the `configure_logging()` call.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the GitHub issues
3. Create a new issue with detailed information