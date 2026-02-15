import os
import sys
from pathlib import Path

# Add the project root to the Python path so we can import base_watcher
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from watchers.base_watcher import BaseWatcher
from datetime import datetime
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil


class FileDropWatcher(FileSystemEventHandler, BaseWatcher):
    def __init__(self, vault_path: str, watch_folder: str):
        BaseWatcher.__init__(self, vault_path, check_interval=10)  # Check every 10 seconds
        self.watch_folder = Path(watch_folder)
        self.needs_action = Path(vault_path) / 'Needs_Action'
        self.observer = Observer()
        
    def start_watching(self):
        """Start watching the specified folder for new files"""
        self.observer.schedule(self, str(self.watch_folder), recursive=False)
        self.observer.start()
        self.logger.info(f'Starting FileDropWatcher for folder: {self.watch_folder}')
        
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            self.logger.info('FileDropWatcher stopped')
        
        self.observer.join()

    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        
        # Skip temporary files
        if source.name.startswith('~') or source.suffix in ['.tmp', '.part', '.swp']:
            return
            
        # Copy file to Needs_Action folder
        dest = self.needs_action / f'FILE_DROP_{source.name}'
        shutil.copy2(source, dest)
        
        # Create metadata file
        self.create_metadata(source, dest)

    def create_metadata(self, source: Path, dest: Path):
        """Create a metadata markdown file for the dropped file"""
        meta_content = f"""---
type: file_drop
original_name: {source.name}
size: {source.stat().st_size}
received: {datetime.now().isoformat()}
status: pending
---

New file dropped for processing: {source.name}

## File Information
- Size: {source.stat().st_size} bytes
- Location: {source.parent}
- Dropped at: {datetime.now().isoformat()}

## Suggested Actions
- [ ] Review file contents
- [ ] Determine appropriate action
- [ ] Process or forward as needed
"""
        
        meta_path = dest.with_name(f'META_FILE_DROP_{source.name}.md')
        meta_path.write_text(meta_content)
        
        self.logger.info(f"Created metadata file for dropped file: {source.name}")

    def check_for_updates(self) -> list:
        # This method is required by BaseWatcher but not used in this implementation
        return []

    def create_action_file(self, item) -> Path:
        # This method is required by BaseWatcher but not used in this implementation
        return None