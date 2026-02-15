# Personal AI Employee - Autonomous FTE (Full-Time Equivalent)

## Overview
This project implements a "Digital FTE" (Full-Time Equivalent) as described in the Personal AI Employee Hackathon. It creates an AI agent powered by Claude Code and Obsidian that proactively manages personal and business affairs 24/7.

## Architecture

### Components
- **The Brain**: Claude Code acts as the reasoning engine
- **The Memory/GUI**: Obsidian (local Markdown) as the dashboard
- **The Senses (Watchers)**: Lightweight Python scripts monitoring Gmail, WhatsApp, and filesystems
- **The Hands (MCP)**: Model Context Protocol servers handle external actions

### Directory Structure
```
AI_Employee_Vault/
├── Dashboard.md              # Real-time summary
├── Company_Handbook.md       # Rules of engagement
├── Business_Goals.md         # Business objectives
├── Needs_Action/             # Items requiring attention
├── Plans/                    # Generated action plans
├── Done/                     # Completed tasks
├── Pending_Approval/         # Actions requiring approval
├── Approved/                 # Approved actions
├── Rejected/                 # Rejected actions
├── Logs/                     # Audit logs
├── Briefings/                # Weekly CEO briefings
└── Accounting/               # Financial records
```

## Features Implemented

### 1. Watcher System
- **Gmail Watcher**: Monitors Gmail for new important emails
- **File Drop Watcher**: Watches for files dropped in specified folders
- **Base Watcher**: Abstract class for creating new watchers

### 2. Orchestration
- **Orchestrator**: Manages all watchers and system status
- **Ralph Wiggum Loop**: Continuous task execution until completion
- **Status Monitoring**: Updates dashboard with system status

### 3. Business Intelligence
- **CEO Briefing Generator**: Weekly business summary
- **Revenue Tracking**: Monitors income and expenses
- **Task Management**: Tracks completed and pending tasks

### 4. Human-in-the-Loop
- **Approval System**: Critical actions require human approval
- **Audit Trail**: All actions logged for review
- **Safety Mechanisms**: Prevents unauthorized actions

## Setup Instructions

### Prerequisites
- Python 3.13+
- Node.js v24+ LTS
- Claude Code subscription
- Obsidian v1.10.6+

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies for MCP servers:
```bash
cd mcp_servers/email-mcp
npm install
```

4. Set up environment variables in `.env`:
```env
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

5. Create Obsidian vault:
- Open Obsidian
- Choose "Open folder as vault"
- Select the `AI_Employee_Vault` directory

## Configuration

### Watchers
To add a Gmail watcher to the orchestrator, uncomment and configure in `orchestrator.py`:

```python
gmail_watcher = GmailWatcher(
    vault_path=Path("./AI_Employee_Vault"),
    email_account=os.getenv("GMAIL_USER"),
    password=os.getenv("GMAIL_APP_PASSWORD")
)
orchestrator.add_watcher(gmail_watcher)
```

### MCP Servers
Configure Claude Code to use MCP servers by placing `mcp_config.json` in the appropriate Claude Code configuration directory.

## Usage

### Running the System
1. Start the orchestrator:
```bash
python orchestrator.py
```

2. The system will:
   - Monitor configured sources (Gmail, file drops, etc.)
   - Create action items in the `Needs_Action` folder
   - Update the dashboard with current status
   - Generate plans and request approvals as needed

### Testing
Run the test file creator to see the system in action:
```bash
python create_test_files.py
```

### CEO Briefing
Generate a weekly business summary:
```bash
python ceo_briefing.py
```

## Security & Privacy

### Credential Management
- Store credentials in environment variables or secure credential managers
- Never commit credentials to version control
- Use app passwords for Gmail instead of account passwords
- Rotate credentials regularly

### Audit Logging
- All actions are logged in the `Logs` directory
- Approval-required actions are documented in `Pending_Approval`
- System status is continuously updated in `Dashboard.md`

## Extending the System

### Adding New Watchers
Create new watchers by extending the `BaseWatcher` class:

```python
from watchers.base_watcher import BaseWatcher

class NewWatcher(BaseWatcher):
    def check_for_updates(self) -> list:
        # Return list of new items to process
        pass

    def create_action_file(self, item) -> Path:
        # Create .md file in Needs_Action folder
        pass
```

### Adding MCP Servers
Create new MCP servers following the Model Context Protocol specification and register them in the configuration.

## Troubleshooting

### Common Issues
- **Gmail API errors**: Ensure you're using an app password, not your regular password
- **File permissions**: Ensure the system has read/write access to the vault directory
- **MCP server not connecting**: Check that the server process is running and the path is correct

### Debugging
- Check `ai_employee.log` for system logs
- Review files in the `Logs` directory for action history
- Verify environment variables are properly set

## Roadmap

### Bronze Tier (Implemented)
- Obsidian vault with Dashboard and Company Handbook
- Working Watcher script (Gmail and file system monitoring)
- Claude Code integration with vault
- Basic folder structure

### Silver Tier (Partially Implemented)
- Multiple Watcher scripts
- Claude reasoning loop for Plan creation
- MCP server for email actions
- Human-in-the-loop approval workflow

### Gold Tier (Future)
- Full cross-domain integration
- Accounting system integration (Odoo)
- Social media posting
- Advanced error recovery
- Ralph Wiggum loop for autonomous completion

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License - see LICENSE file for details