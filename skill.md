# AI Employee Agent Skills Documentation

## Overview
This document describes the various agent skills implemented in the AI Employee system. These skills represent the core AI functionalities that enable the system to operate autonomously.

## Available Skills

### 1. File Reading Skill (`read_file`)
- **Purpose**: Read content from a file in the vault
- **Parameters**: `file_path` - Path to the file to read
- **Returns**: Success status, file content, and file path
- **Usage**: Used to access information stored in the vault

### 2. File Writing Skill (`write_file`)
- **Purpose**: Write content to a file in the vault
- **Parameters**: `file_path` - Destination path, `content` - Content to write
- **Returns**: Success status and file path
- **Usage**: Used to store information and create new documents in the vault

### 3. File Moving Skill (`move_file`)
- **Purpose**: Move a file from one location to another in the vault
- **Parameters**: `source_path` - Source file path, `destination_folder` - Destination folder
- **Returns**: Success status and paths
- **Usage**: Used to organize files as they transition between states (e.g., from Needs_Action to Done)

### 4. File Search Skill (`search_files`)
- **Purpose**: Search for files in a specific folder
- **Parameters**: `folder_path` - Folder to search in, `pattern` - File pattern to match (default: *.md)
- **Returns**: Success status, folder path, pattern, file list, and count
- **Usage**: Used to discover files that need processing

### 5. Dashboard Update Skill (`update_dashboard`)
- **Purpose**: Update the system dashboard with current status
- **Parameters**: `status_updates` - Dictionary of status updates to apply
- **Returns**: Success status and message
- **Usage**: Used to keep stakeholders informed of system status

### 6. Action Item Creation Skill (`create_action_item`)
- **Purpose**: Create a new action item in the Needs_Action folder
- **Parameters**: `title`, `description`, `priority` (default: medium), `category` (default: general)
- **Returns**: Success status and file path
- **Usage**: Used to create tasks for the system to process

## Skill Implementation Details

All skills are implemented in the `agent_skills.py` file as methods of the `AgentSkills` class. Each skill follows a consistent pattern:

- Accepts specific parameters relevant to its function
- Performs validation and error handling
- Returns a standardized result dictionary with success status and relevant data
- Logs actions for audit purposes

## Usage Examples

### Creating an Action Item
```python
agent = AgentSkills()
result = agent.create_action_item(
    title="Process Invoice Request",
    description="Handle client request for invoice generation",
    priority="high",
    category="finance"
)
```

### Moving a File
```python
agent = AgentSkills()
result = agent.move_file(
    source_path="Needs_Action/invoice_request.md",
    destination_folder="Done"
)
```

### Updating Dashboard
```python
agent = AgentSkills()
status_updates = {
    "AI Employee": "Online",
    "Active Watchers": 1,
    "Pending Actions": 3
}
agent.update_dashboard(status_updates)
```

## Integration with System Components

These agent skills are integrated with other system components:

- **Watchers**: Use skills to create action items when new inputs are detected
- **Orchestrator**: Coordinates the execution of skills based on system state
- **Vault Operations**: Enable reading and writing of information in the vault

## Error Handling

Each skill implements comprehensive error handling:
- Validation of input parameters
- Checking for file/folder existence
- Handling of file system permissions
- Recovery from common failure modes

## Future Enhancements

Potential additional skills that could be implemented:
- Email sending/receiving capabilities
- Calendar management
- Web scraping and data extraction
- Integration with external APIs
- Natural language processing for content analysis