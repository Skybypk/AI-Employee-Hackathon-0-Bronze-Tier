# AI Employee Bronze Tier Specification Kit

## Project Overview
This specification kit outlines the Bronze Tier implementation of the AI Employee system as defined in the hackathon requirements.

## Bronze Tier Requirements
The Bronze Tier represents the Foundation or Minimum Viable Deliverable with the following components:

### 1. Vault with Dashboard.md and Company_Handbook.md
- **Dashboard.md**: Real-time system status dashboard
- **Company_Handbook.md**: Rules of engagement and operational procedures
- Both files located in the AI_Employee_Vault directory

### 2. One Working Watcher Script
- **Inbox Watcher**: Monitors the Inbox folder for new files
- Moves files from Inbox to Needs_Action
- Creates metadata files for proper tracking
- Located in watchers/inbox_watcher.py

### 3. Qwen Code Reading from and Writing to the Vault
- Implemented in vault_operations_demo.py
- Demonstrates read/write capabilities to the vault
- Proper file handling with error checking

### 4. Basic Folder Structure
- `/Inbox`: Incoming items to be processed
- `/Needs_Action`: Items requiring attention
- `/Done`: Completed tasks
- All folders located in AI_Employee_Vault directory

### 5. AI Functionality as Agent Skills
- Implemented in agent_skills.py
- Modular skill-based architecture
- Includes file operations, dashboard updates, and action item creation

## Technical Specifications

### System Requirements
- Python 3.10 or higher
- Windows, macOS, or Linux operating system
- At least 1GB free disk space for vault storage

### Dependencies
- watchdog>=3.0.0 (for file system monitoring)
- python-dotenv>=1.0.0 (for environment variable management)
- requests>=2.31.0 (for HTTP requests if needed)

### File Structure
```
AI_Employee_Project/
├── agent_skills.py          # AI functionality as skills
├── bronze_tier.py          # Main Bronze Tier implementation
├── vault_operations_demo.py # Qwen Code vault operations
├── orchestrator.py         # System orchestrator
├── BRONZE_TIER_IMPLEMENTATION.md # Documentation
├── skill.md                # Skills documentation
├── README.md               # Project overview
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── pyproject.toml         # Project configuration
├── uv.lock                # Package lock file
├── .python-version        # Python version specification
├── AI_Employee_Vault/     # The vault directory
│   ├── Dashboard.md       # System dashboard
│   ├── Company_Handbook.md # Rules of engagement
│   ├── Inbox/             # Incoming items
│   ├── Needs_Action/      # Items requiring attention
│   └── Done/              # Completed tasks
└── watchers/              # Watcher scripts
    ├── base_watcher.py    # Base watcher class
    └── inbox_watcher.py   # Inbox monitoring watcher
```

## Implementation Details

### Agent Skills
The AI functionality is implemented as modular skills:
- `read_file()`: Read content from vault files
- `write_file()`: Write content to vault files
- `move_file()`: Move files between vault directories
- `search_files()`: Search for files in specific folders
- `update_dashboard()`: Update system status dashboard
- `create_action_item()`: Create new tasks for processing

### Watcher System
The watcher system monitors the vault for changes:
- Extends the BaseWatcher abstract class
- Implements file system monitoring capabilities
- Creates action items when new content is detected

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Bronze Tier implementation: `python bronze_tier.py`

## Quality Assurance

### Testing Approach
- Manual verification of all Bronze Tier requirements
- Functional testing of each agent skill
- Integration testing of watcher system
- Vault operations validation

### Success Criteria
- All five Bronze Tier requirements implemented
- System operates without errors
- Files properly read from and written to vault
- Watcher detects and processes new files
- Agent skills function as expected

## Maintenance Guidelines

### Updating the System
- Modify agent skills in agent_skills.py for new capabilities
- Extend watcher functionality in the watchers/ directory
- Update documentation as needed

### Troubleshooting
- Check AI_Employee_Vault directory permissions
- Verify Python dependencies are installed
- Review log files for error details

## Next Steps

With Bronze Tier complete, the system is ready for Silver Tier enhancements including:
- Multiple Watcher scripts
- Claude reasoning loop for Plan creation
- MCP server for email actions
- Human-in-the-loop approval workflow