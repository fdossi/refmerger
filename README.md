# RefMerger: Bibliographic Reference Processing Tool

**RefMerger** is a robust and free Python tool for researchers, librarians, and academics working with large volumes of bibliographic references. It automates the tedious process of merging references from multiple sources and removing duplicates, saving hours of manual work.

## Detailed Description

In research projects, it is common to collect references from various sources such as PubMed, Web of Science, Scopus, or local databases. Each source exports in different formats (.bib, .xml, .csv, .json), and when joining them, inevitable duplicates arise. RefMerger solves this by converting everything to RIS format (standard for reference managers like Zotero, Mendeley, and EndNote), merging the files, and applying intelligent deduplication.

### Main Benefits:
- **Multi-Format Support**: Automatically converts .bib (BibTeX), .xml (PubMed), .csv, .json, and .ris
- **Advanced Deduplication**: Uses similarity algorithms to detect duplicates even with title variations or formatting
- **Flexibility**: Configurable deduplication modes for different needs
- **Robust**: Handles various encodings and file errors gracefully
- **Free and Open-Source**: Pure Python code, no heavy dependencies

## Features

- **Format Conversion**: Supports .ris, .bib, .xml, .csv, .json
- **File Merging**: Combines multiple files into a single RIS
- **Robust Deduplication**: Removes duplicates with priority DOI > PMID > Title+Year+Author > Hash
- **Deduplication Modes**:
  - `strict`: DOI only
  - `balanced`: DOI + Title/Year/Author
  - `aggressive`: Includes title similarity (90%+)
- **Export**: To CSV or JSON (optional)
- **Encoding Detection**: UTF-8, Latin-1, Windows-1252

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/fdossi/refmerger.git
   cd refmerger
   ```

2. **Install dependencies** (optional, only for .bib):
   ```bash
   pip install bibtexparser
   ```

3. **Run the script**:
   ```bash
   python refmerger.py
   ```

## How to Use

1. Place all files (.ris, .bib, .xml, .csv, .json) in the same folder.
2. Edit the variables at the end of the script:
   - `pasta_dos_arquivos`: Folder path
   - `modo_deduplicacao`: 'strict', 'balanced', or 'aggressive'
   - `formato_exportar`: None (RIS), 'csv', or 'json'
3. Run the Python script.

### Usage Example:
```python
# Settings at the end of refmerger.py
pasta_dos_arquivos = r"C:\My\Files\References"
modo_deduplicacao = 'balanced'
formato_exportar = None  # Output in RIS
```

Expected output:
```
Success! 25 files were merged into 'todas_referencias_juntas.ris'.
707 duplicate reference(s) removed. Final total: 268 unique reference(s).
```

## Dependencies

- Python 3.x
- bibtexparser (for .bib): `pip install bibtexparser`
- Standard libraries: os, glob, re, json, csv, xml.etree, unicodedata, hashlib, difflib

## Example Output

```
Success! 25 files were merged into 'todas_referencias_juntas.ris'.
707 duplicate reference(s) removed. Final total: 268 unique reference(s).
```

## Supported Formats

### .bib (BibTeX)
Fields: title, author, year, doi, journal

### .xml (PubMed)
Expected structure: ArticleTitle, Author/LastName, Year, DOI

### .csv
Columns: title, authors (separated by ;), year, doi

### .json
Structure: [{"title": "...", "authors": [...], "year": "...", "doi": "..."}]

## Contribution

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Developed by Fábio Dossi.

Note: If this tool assists in your research, feel free to cite it in your paper. It’s **entirely optional**, but always appreciated!

APA (7th Edition)
Dossi, F. C. A. (2026). RefMerger (Version 1.0.0) [Computer software]. GitHub. https://github.com/fdossi/refmerger

BibTeX (For LaTeX users)
@software{Dossi_RefMerger_2026,
  author = {Dossi, F. C. A.},
  title = {{RefMerger: Automating reference merging and deduplication}},
  url = {https://github.com/fdossi/refmerger},
  version = {1.0.0},
  year = {2026}
}

ABNT (Brazil)
DOSSI, Fabio F. C. A. RefMerger: a tool for automating the merging and deduplication of references. Version 1.0.0. Aracaju, 2026. Available at: https://github.com/fdossi/refmerger. Accessed on: Apr. 23, 2026.

MLA (9th Edition)
Dossi, F. C. A. RefMerger. Version 1.0.0, 2026, github.com/fdossi/refmerger.