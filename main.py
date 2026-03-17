import os
import json
import logging
import re
from datetime import datetime

try:
    from exporter import EvernoteExporter
except ImportError:
    logging.error("exporter module not found. Please ensure exporter.py exists.")
    exit(1)

try:
    from config import Config
except ImportError:
    logging.error("config module not found. Please ensure config.py exists.")
    exit(1)

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sanitize_filename(filename):
    """Remove or replace invalid characters for filesystem"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def main():
    # Load configuration
    try:
        config = Config.load()
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        return

    # Check if the necessary directories exist
    if not os.path.exists(config.export_directory):
        os.makedirs(config.export_directory)
        logging.info(f"Created export directory: {config.export_directory}")

    # Initialize the Evernote exporter
    exporter = EvernoteExporter(config)

    # Export notes
    try:
        notes = exporter.fetch_notes()
        logging.info(f"Fetched {len(notes)} notes from Evernote.")
        
        exported_files = set()
        for note in notes:
            try:
                markdown_content = exporter.export_to_markdown(note)
                safe_title = sanitize_filename(note.title)
                
                # Handle duplicate filenames
                base_filename = safe_title
                counter = 1
                while safe_title in exported_files:
                    safe_title = f"{base_filename}_{counter}"
                    counter += 1
                exported_files.add(safe_title)
                
                file_path = os.path.join(config.export_directory, f"{safe_title}.md")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                logging.info(f"Exported note '{note.title}' to {file_path}.")
            except Exception as e:
                logging.error(f"Failed to export note '{note.title}': {e}")
                
    except Exception as e:
        logging.error(f"Failed to fetch notes: {e}")

if __name__ == "__main__":
    main()
