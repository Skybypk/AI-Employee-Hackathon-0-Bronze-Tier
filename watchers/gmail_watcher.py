import os
import sys
from pathlib import Path

# Add the project root to the Python path so we can import base_watcher
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from watchers.base_watcher import BaseWatcher
from datetime import datetime
import imaplib
import email
from email.header import decode_header


class GmailWatcher(BaseWatcher):
    def __init__(self, vault_path: str, email_account: str, password: str, imap_server: str = "imap.gmail.com"):
        super().__init__(vault_path, check_interval=120)  # Check every 2 minutes
        self.email_account = email_account
        self.password = password
        self.imap_server = imap_server
        self.processed_ids = set()
        
        # Connect to the IMAP server
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_account, self.password)
            self.mail.select('INBOX')
        except Exception as e:
            self.logger.error(f"Failed to connect to Gmail: {e}")
            raise

    def check_for_updates(self) -> list:
        """Check for new unread emails"""
        try:
            # Search for unread emails
            status, messages = self.mail.search(None, 'UNSEEN')
            if status != 'OK':
                return []
                
            email_ids = messages[0].split()
            
            # Filter out emails we've already processed
            new_emails = []
            for email_id in email_ids:
                email_str = email_id.decode()
                if email_str not in self.processed_ids:
                    new_emails.append(email_id)
                    self.processed_ids.add(email_str)
                    
            return new_emails
        except Exception as e:
            self.logger.error(f"Error checking for emails: {e}")
            # Reconnect if connection was lost
            try:
                self.mail = imaplib.IMAP4_SSL(self.imap_server)
                self.mail.login(self.email_account, self.password)
                self.mail.select('INBOX')
            except Exception as reconnect_error:
                self.logger.error(f"Failed to reconnect: {reconnect_error}")
            return []

    def create_action_file(self, email_id) -> Path:
        """Create a markdown file for the email in Needs_Action folder"""
        try:
            # Fetch the email
            status, msg_data = self.mail.fetch(email_id, '(RFC822)')
            if status != 'OK':
                return None
                
            # Parse the email
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extract email information
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
                
            sender = msg.get("From", "Unknown Sender")
            date_received = msg.get("Date", datetime.now().isoformat())
            
            # Extract email body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode(errors='ignore')
                            break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors='ignore')
            
            # Determine priority based on subject keywords
            high_priority_keywords = ['urgent', 'asap', 'immediate', 'critical', 'emergency', 'payment', 'invoice']
            priority = 'high' if any(keyword in subject.lower() for keyword in high_priority_keywords) else 'medium'
            
            # Create the markdown content
            content = f"""---
type: email
from: {sender}
subject: {subject}
received: {date_received}
priority: {priority}
status: pending
---

## Email Content
{body}

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
"""
            
            # Create filename with email ID
            filepath = self.needs_action / f'EMAIL_{email_id.decode()}.md'
            filepath.write_text(content)
            
            self.logger.info(f"Created action file for email: {subject[:50]}...")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")
            return None

    def close(self):
        """Close the IMAP connection"""
        try:
            self.mail.close()
            self.mail.logout()
        except:
            pass  # Connection might already be closed