import os
import sys
from pathlib import Path

# Add the project root to the Python path so we can import base_watcher
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from watchers.base_watcher import BaseWatcher
from datetime import datetime
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class InboxWatcher(FileSystemEventHandler, BaseWatcher):
    def __init__(self, vault_path: str):
        BaseWatcher.__init__(self, vault_path, check_interval=10)  # Check every 10 seconds
        self.inbox = Path(vault_path) / 'Inbox'
        self.needs_action = Path(vault_path) / 'Needs_Action'
        self.observer = Observer()

    def start_watching(self):
        """Start watching the inbox folder for new files"""
        self.observer.schedule(self, str(self.inbox), recursive=False)
        self.observer.start()
        self.logger.info(f'Starting InboxWatcher for folder: {self.inbox}')

        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            self.logger.info('InboxWatcher stopped')

        self.observer.join()

    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)

        # Skip temporary files
        if source.name.startswith('~') or source.suffix in ['.tmp', '.part', '.swp']:
            return

        # Move file to Needs_Action folder
        dest = self.needs_action / source.name
        shutil.move(source, dest)

        # Create metadata file
        self.create_action_file(dest)

        self.logger.info(f"Moved file from Inbox to Needs_Action: {source.name}")

    def on_modified(self, event):
        # Handle file modifications if needed
        pass

    def check_for_updates(self) -> list:
        # This method is required by BaseWatcher but not used in this implementation
        return []

    def create_action_file(self, file_path) -> Path:
        """Create a metadata markdown file for the moved file"""
        # Create metadata content
        meta_content = f"""---
type: inbox_file
original_name: {file_path.name}
size: {file_path.stat().st_size}
received: {datetime.now().isoformat()}
status: pending
---

New file received in Inbox: {file_path.name}

## File Information
- Size: {file_path.stat().st_size} bytes
- Location: {file_path.parent}
- Received at: {datetime.now().isoformat()}

## Suggested Actions
- [ ] Review file contents
- [ ] Determine appropriate action
- [ ] Process or forward as needed
"""

        # Create metadata file in Needs_Action folder
        meta_path = self.needs_action / f'META_{file_path.name}.md'
        meta_path.write_text(meta_content)

        self.logger.info(f"Created action file for: {file_path.name}")
        return meta_path