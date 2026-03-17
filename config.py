import os

class Config:
    def __init__(self):
        # Load configuration from environment variables or set defaults
        self.evernote_api_key = os.getenv('EVERNOTE_API_KEY', 'your_api_key_here')
        self.evernote_api_secret = os.getenv('EVERNOTE_API_SECRET', 'your_api_secret_here')
        self.output_directory = os.getenv('OUTPUT_DIRECTORY', './exported_notes')
        
        # Ensure output directory exists
        if not os.path.exists(self.output_directory):
            try:
                os.makedirs(self.output_directory)
            except Exception as e:
                raise RuntimeError(f"Could not create output directory: {e}")

    def validate(self):
        # Simple validation of required fields
        if (not self.evernote_api_key or 
            not self.evernote_api_secret or 
            self.evernote_api_key == 'your_api_key_here' or 
            self.evernote_api_secret == 'your_api_secret_here'):
            raise ValueError("Evernote API key and secret must be set.")

    def __str__(self):
        return f"Config(evernote_api_key={'*' * len(self.evernote_api_key) if self.evernote_api_key else 'None'}, output_directory={self.output_directory})"

# Usage example (this won't run as part of the config file, it's just here for clarity):
# if __name__ == "__main__":
#     config = Config()
#     config.validate()
#     print(config) 

# TODO: Consider adding support for loading from a config file (e.g., JSON, YAML).
# TODO: Implement logging for better error tracking and debugging.
