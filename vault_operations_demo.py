import os
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def read_from_vault(file_path):
    """
    Reads content from a file in the vault
    """
    vault_path = Path("./AI_Employee_Vault")
    full_path = vault_path / file_path
    
    if full_path.exists():
        content = full_path.read_text(encoding='utf-8')
        print(f"Successfully read from: {full_path}")
        return content
    else:
        print(f"File does not exist: {full_path}")
        return None

def write_to_vault(file_path, content):
    """
    Writes content to a file in the vault
    """
    vault_path = Path("./AI_Employee_Vault")
    full_path = vault_path / file_path
    
    # Create parent directories if they don't exist
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the content to the file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Successfully wrote to: {full_path}")
    return full_path

def demonstrate_vault_operations():
    """
    Demonstrates reading from and writing to the vault
    """
    print("Demonstrating Qwen Code functionality for vault operations...\n")
    
    # 1. Read from Company_Handbook.md
    print("1. Reading from Company_Handbook.md:")
    handbook_content = read_from_vault("Company_Handbook.md")
    if handbook_content:
        print(f"Content preview: {handbook_content[:200]}...\n")
    
    # 2. Read from Dashboard.md
    print("2. Reading from Dashboard.md:")
    dashboard_content = read_from_vault("Dashboard.md")
    if dashboard_content:
        print(f"Content preview: {dashboard_content[:200]}...\n")
    
    # 3. Write a test file to the Needs_Action folder
    print("3. Writing a test file to Needs_Action folder:")
    test_content = f"""---
type: test_item
created: {datetime.now().isoformat()}
status: pending
---

## Test Item Created by Qwen Code

This is a test file demonstrating Qwen Code's ability to write to the vault.

### Details
- Created at: {datetime.now().isoformat()}
- Purpose: Demonstrate write functionality
- Status: Ready for processing

### Actions Required
- [ ] Review this test item
- [ ] Process according to Company Handbook
- [ ] Move to Done when completed
"""
    
    file_path = write_to_vault("Needs_Action/TEST_Qwen_Code_Functionality.md", test_content)
    
    # 4. Read the file we just created
    print("\n4. Reading the file we just created:")
    created_content = read_from_vault("Needs_Action/TEST_Qwen_Code_Functionality.md")
    if created_content:
        print(f"Content: {created_content}")
    
    print("\nDemonstration complete!")

if __name__ == "__main__":
    demonstrate_vault_operations()