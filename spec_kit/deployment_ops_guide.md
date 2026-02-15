# AI Employee Bronze Tier Deployment & Operations Guide

## Overview
This document provides comprehensive guidance for deploying and operating the Bronze Tier implementation of the AI Employee system in production environments.

## Deployment Scenarios

### 1. Local Development Deployment
**Target**: Individual developer workstation
**Purpose**: Development, testing, and validation
**Requirements**: Local Python environment

### 2. Standalone Server Deployment
**Target**: Dedicated server or VM
**Purpose**: Production operation
**Requirements**: Server with Python runtime

### 3. Containerized Deployment
**Target**: Docker-enabled environment
**Purpose**: Portable and scalable deployment
**Requirements**: Docker and container orchestration platform

## Pre-Deployment Checklist

### Infrastructure Requirements
- [ ] Server/VM with appropriate resources (CPU, RAM, disk)
- [ ] Python 3.10+ installed and accessible
- [ ] Network connectivity for external integrations (if applicable)
- [ ] Adequate disk space for vault storage and logs
- [ ] Backup solution configured

### Security Preparations
- [ ] User account with limited privileges created
- [ ] Firewall rules configured for application access
- [ ] SSL certificates installed (if required)
- [ ] Antivirus exclusions set for vault directory
- [ ] Audit logging enabled

### Application Preparation
- [ ] Latest code version pulled from repository
- [ ] Dependencies installed via requirements.txt
- [ ] Configuration files reviewed and customized
- [ ] Vault directory structure created
- [ ] Initial dashboard and handbook files created

## Deployment Process

### Step 1: Environment Setup
```bash
# Clone the repository
git clone https://github.com/your-organization/ai-employee-hackathon.git
cd ai-employee-hackathon

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configuration
```bash
# Create vault directory structure
mkdir -p AI_Employee_Vault/{Inbox,Needs_Action,Done}

# Create initial dashboard and handbook files
cp templates/Dashboard.md AI_Employee_Vault/
cp templates/Company_Handbook.md AI_Employee_Vault/
```

### Step 3: Initial Validation
```bash
# Run the bronze tier implementation to verify setup
python bronze_tier.py
```

### Step 4: Service Configuration
For production deployments, configure the system as a service:

**Linux systemd service** (`/etc/systemd/system/ai-employee.service`):
```
[Unit]
Description=AI Employee Service
After=network.target

[Service]
Type=simple
User=ai-employee
WorkingDirectory=/opt/ai-employee
Environment=PATH=/opt/ai-employee/venv/bin
ExecStart=/opt/ai-employee/venv/bin/python bronze_tier.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-employee
sudo systemctl start ai-employee
```

## Configuration Management

### Main Configuration File
Create a `config.json` file in the root directory:

```json
{
  "vault_path": "./AI_Employee_Vault",
  "watchers": {
    "inbox_check_interval": 10,
    "enable_gmail": false,
    "gmail_check_interval": 120
  },
  "logging": {
    "level": "INFO",
    "file": "ai_employee.log",
    "max_size_mb": 100,
    "backup_count": 5
  },
  "security": {
    "enable_audit_logging": true,
    "credentials_path": "./.env"
  }
}
```

### Environment Variables
For sensitive information, use environment variables:

```
# Gmail credentials (if enabled)
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password

# Vault location (if different from default)
VAULT_PATH=/path/to/vault

# Logging configuration
LOG_LEVEL=INFO
```

## Operational Procedures

### Daily Operations

#### 1. System Health Check
```bash
# Check if the service is running
systemctl status ai-employee

# Check log files for errors
tail -f ai_employee.log

# Verify vault disk space
df -h AI_Employee_Vault/
```

#### 2. Dashboard Review
- Review Dashboard.md for system status
- Check pending action counts
- Verify active watchers status

#### 3. Log Analysis
- Review log files for errors or warnings
- Check for failed operations
- Monitor system performance metrics

### Weekly Operations

#### 1. Backup Verification
- Verify automated backups are running
- Test backup restoration process
- Check backup storage space

#### 2. Performance Review
- Analyze system performance metrics
- Review processing times for actions
- Check resource utilization trends

#### 3. Security Audit
- Review access logs
- Check for unauthorized access attempts
- Verify credential security

### Monthly Operations

#### 1. System Maintenance
- Clean up old log files
- Optimize vault storage
- Update dependencies if needed

#### 2. Capacity Planning
- Review vault growth trends
- Plan for additional storage if needed
- Assess performance requirements

## Monitoring and Alerting

### Key Metrics to Monitor
- System uptime
- Vault disk usage
- Number of pending actions
- Processing success rate
- Error rates

### Alerting Thresholds
- Disk usage > 80%: Warning
- Disk usage > 90%: Critical
- Error rate > 5%: Warning
- Error rate > 10%: Critical
- System downtime > 5 minutes: Critical

### Monitoring Scripts
Create monitoring scripts to check system health:

```bash
#!/bin/bash
# health_check.sh

VAULT_PATH="./AI_Employee_Vault"
CRITICAL_THRESHOLD=90
WARNING_THRESHOLD=80

# Check disk usage
DISK_USAGE=$(df "$VAULT_PATH" | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt "$CRITICAL_THRESHOLD" ]; then
    echo "CRITICAL: Vault disk usage is ${DISK_USAGE}%"
    exit 2
elif [ "$DISK_USAGE" -gt "$WARNING_THRESHOLD" ]; then
    echo "WARNING: Vault disk usage is ${DISK_USAGE}%"
    exit 1
else
    echo "OK: Vault disk usage is ${DISK_USAGE}%"
    exit 0
fi
```

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue: Permission Denied Errors
**Symptoms**: System cannot read/write to vault
**Causes**: Incorrect file permissions
**Solution**: 
```bash
# Set proper permissions on vault directory
chmod -R 755 AI_Employee_Vault/
chown -R ai-employee:ai-employee AI_Employee_Vault/
```

#### Issue: High Memory Usage
**Symptoms**: System slows down or crashes
**Causes**: Large files in vault or memory leaks
**Solution**: 
- Check for unusually large files in vault
- Restart the service
- Monitor memory usage patterns

#### Issue: Watcher Not Detecting Changes
**Symptoms**: Files in Inbox not being processed
**Causes**: File system monitoring issues
**Solution**:
- Verify the watcher service is running
- Check file permissions in Inbox directory
- Restart the watcher service

#### Issue: Dashboard Not Updating
**Symptoms**: Dashboard shows stale information
**Causes**: Agent skills not updating dashboard
**Solution**:
- Verify agent skills are functioning
- Check for errors in log files
- Manually trigger dashboard update

### Diagnostic Commands
```bash
# Check system status
python -c "from bronze_tier import setup_bronze_tier; setup_bronze_tier()"

# Verify vault structure
ls -la AI_Employee_Vault/

# Test agent skills
python -c "from agent_skills import AgentSkills; agent = AgentSkills(); print('Agent skills working:', agent.search_files('Needs_Action'))"

# Check file counts
find AI_Employee_Vault/Needs_Action -name '*.md' | wc -l
```

## Backup and Recovery

### Backup Strategy
- Full vault backup daily
- Incremental backups every 4 hours
- Off-site backup storage
- Retention: 30 days for daily backups, 1 year for weekly

### Backup Script
```bash
#!/bin/bash
# backup_vault.sh

BACKUP_DIR="/backup/ai_employee"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="vault_backup_$DATE.tar.gz"

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_NAME" AI_Employee_Vault/

# Remove backups older than 30 days
find "$BACKUP_DIR" -name "vault_backup_*.tar.gz" -mtime +30 -delete
```

### Recovery Procedure
1. Stop the AI Employee service
2. Restore vault from backup
3. Verify file permissions
4. Restart the service
5. Validate system functionality

## Scaling Considerations

### Current (Bronze Tier) Limitations
- Single-threaded operation
- Local file system storage
- Basic monitoring capabilities

### Scaling Indicators
- Consistently high pending action counts (>100)
- Slow processing times (>5 minutes per action)
- High resource utilization (>80%)

### Scaling Options
1. **Vertical Scaling**: Increase server resources
2. **Horizontal Scaling**: Deploy multiple instances for different functions
3. **Storage Scaling**: Implement cloud storage solutions

## Decommissioning Process

### Planned Decommissioning
1. Stop all services
2. Process all pending actions
3. Create final backup
4. Document system state
5. Transfer ownership of data if required

### Emergency Decommissioning
1. Immediate service stop
2. Emergency backup of vault
3. Incident documentation
4. Root cause analysis

## Conclusion
This deployment and operations guide provides the necessary procedures for successfully deploying and operating the Bronze Tier AI Employee system. Following these procedures will ensure reliable operation and easy maintenance of the system.