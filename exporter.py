import os
import sys
import logging
import re
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO)

class EvernoteExporter:
    def __init__(self, token, output_dir):
        self.client = EvernoteClient(token=token, sandbox=False)
        self.output_dir = output_dir

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_notes(self):
        """Fetch all notes from the user's Evernote account."""
        note_store = self.client.get_note_store()
        notes = []

        try:
            # Fetch the user's notes with proper filter
            filter = NoteFilter()
            notes_metadata = note_store.findNotesMetadata(filter, 0, 10000, None)
            
            # Get full note content for each note
            for note_metadata in notes_metadata.notes:
                note = note_store.getNote(note_metadata.guid, True, True, False, False)
                notes.append(note)

            logging.info(f"Fetched {len(notes)} notes.")
        except Exception as e:
            logging.error(f"Failed to fetch notes: {e}")
            sys.exit(1)

        return notes

    def sanitize_filename(self, filename):
        """Remove invalid characters from filename."""
        return re.sub(r'[<>:"/\\|?*]', '_', filename).replace(' ', '_')

    def enml_to_text(self, enml_content):
        """Convert ENML to plain text."""
        if not enml_content:
            return ""
        soup = BeautifulSoup(enml_content, 'xml')
        return soup.get_text()

    def export_to_markdown(self, notes):
        """Export notes to Markdown format."""
        for note in notes:
            try:
                # Convert ENML content to plain text
                text_content = self.enml_to_text(note.content)
                
                file_name = f"{self.sanitize_filename(note.title)}.md"
                file_path = os.path.join(self.output_dir, file_name)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                    logging.info(f"Exported note '{note.title}' to '{file_path}'")
            except Exception as e:
                logging.error(f"Failed to export note '{note.title}': {e}")
    
    def run(self):
        """Main method to run the export process."""
        notes = self.fetch_notes()
        self.export_to_markdown(notes)

if __name__ == "__main__":
    # TODO: Replace with actual Evernote developer token and desired output directory
    EVERNOTE_DEV_TOKEN = "your_evernote_developer_token_here"
    OUTPUT_DIRECTORY = "exported_notes"

    exporter = EvernoteExporter(EVERNOTE_DEV_TOKEN, OUTPUT_DIRECTORY)
    exporter.run()
