# AI Employee System Architecture Specification

## Overview
This document details the architectural design of the AI Employee system, focusing on the Bronze Tier implementation.

## System Architecture

### High-Level Components
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   External      │    │   AI Employee    │    │     Vault       │
│   Inputs        │───▶│     System       │───▶│   (Obsidian)    │
│ (Email, Files)  │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Orchestrator    │
                       │                  │
                       └──────────────────┘
                              │
                   ┌──────────┴──────────┐
                   ▼                     ▼
            ┌─────────────┐      ┌──────────────┐
            │   Watcher   │      │ Agent Skills │
            │   System    │      │   Engine     │
            └─────────────┘      └──────────────┘
```

### Component Descriptions

#### 1. Input Sources
- **Email System**: Monitored by Gmail Watcher
- **File System**: Monitored by FileDrop and Inbox Watchers
- **User Interface**: Obsidian vault for manual input

#### 2. Orchestrator
- **Role**: Central coordinator for all system components
- **Responsibilities**:
  - Manages watcher lifecycle
  - Coordinates system status updates
  - Handles inter-component communication

#### 3. Watcher System
- **BaseWatcher**: Abstract class defining the watcher interface
- **Specialized Watchers**:
  - GmailWatcher: Monitors email accounts
  - FileDropWatcher: Monitors file system changes
  - InboxWatcher: Monitors the Inbox folder

#### 4. Agent Skills Engine
- **Role**: Executes AI-driven actions
- **Skill Types**:
  - File operations (read, write, move)
  - Status updates
  - Action item creation

#### 5. Vault Storage
- **Dashboard.md**: Real-time system status
- **Company_Handbook.md**: Rules and procedures
- **Folder Structure**:
  - Inbox: Incoming items
  - Needs_Action: Items requiring processing
  - Done: Completed tasks

## Data Flow

### Inbound Flow (Input → Processing)
1. Watchers detect new inputs in monitored sources
2. Watchers create action items in Needs_Action folder
3. System updates dashboard with new pending items
4. AI agent processes action items based on Company Handbook

### Outbound Flow (Processing → Output)
1. AI agent executes actions based on skill set
2. Processed items are moved from Needs_Action to Done
3. Dashboard is updated with processing status
4. Outputs are generated (emails, files, etc.)

## Interfaces

### Internal Interfaces
- **Watcher ↔ Orchestrator**: Event notification and coordination
- **Skills Engine ↔ Vault**: File read/write operations
- **Orchestrator ↔ Dashboard**: Status updates

### External Interfaces
- **Email APIs**: For Gmail integration
- **File System APIs**: For file monitoring
- **User Interface**: Obsidian vault access

## Security Considerations

### Access Control
- File system permissions for vault access
- Encrypted storage of sensitive information
- Authentication for external service access

### Data Protection
- Regular backup of vault contents
- Audit logging of all system actions
- Secure handling of credentials

## Scalability Considerations

### Current (Bronze Tier)
- Single-threaded operation
- Local file system storage
- Basic monitoring capabilities

### Future (Silver/Gold Tier)
- Multi-threaded watcher operations
- Cloud storage integration
- Advanced AI reasoning capabilities