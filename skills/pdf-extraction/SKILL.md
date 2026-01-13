---
name: pdf-extraction
description: Extract text, tables, and data from PDF documents
version: 1.0.0
author: Shared Agent Toolkit
tags: [pdf, extraction, data-processing, documents]
---

# PDF Extraction Skill

This skill provides capabilities for extracting text, tables, and structured data from PDF documents, particularly useful for construction documents, specifications, and reports.

## Capabilities

- **Text extraction** - Extract all text or specific pages
- **Table extraction** - Identify and extract tabular data
- **Specification parsing** - Extract construction specifications
- **Metadata extraction** - Get PDF properties and info
- **Search and filter** - Find specific content or patterns
- **OCR support** - Extract text from scanned documents (when available)

## Prerequisites

Python 3.7+ with:
- `pypdf` or `PyPDF2` - Basic PDF text extraction
- `pdfplumber` - Table extraction (recommended)
- `tabula-py` - Advanced table extraction (requires Java)
- `pytesseract` - OCR for scanned PDFs (optional)

## Usage Instructions

When a user needs to extract data from PDFs:

### 1. Identify Document Type
- **Text-based PDF** - Can copy/paste text from the PDF
- **Scanned PDF** - PDF is an image, requires OCR
- **Mixed PDF** - Contains both text and scanned pages

### 2. Determine Extraction Needs
- **Full text** - Extract all content
- **Specific pages** - Extract selected pages
- **Tables** - Extract tabular data to Excel/CSV
- **Specifications** - Parse structured specification documents
- **Search** - Find specific content or patterns

### 3. Choose Appropriate Tool

```bash
# Extract text from PDF
python scripts/extract_text.py --file "spec.pdf" --pages "1-10"

# Extract tables
python scripts/extract_tables.py --file "bid_tab.pdf" --output "tables.xlsx"

# Search PDF content
python scripts/search_pdf.py --file "spec.pdf" --query "prevailing wage"

# Extract CALTRANS specifications
python scripts/extract_spec.py --file "specs.pdf" --format "caltrans"
```

## Common Patterns

### Pattern 1: Extract All Text
```python
import pdfplumber

with pdfplumber.open('document.pdf') as pdf:
    full_text = ''
    for page in pdf.pages:
        full_text += page.extract_text() + '\n'

print(full_text)
```

### Pattern 2: Extract Tables
```python
import pdfplumber

with pdfplumber.open('bid_tab.pdf') as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        tables = page.extract_tables()
        for i, table in enumerate(tables):
            print(f"Page {page_num}, Table {i+1}")
            for row in table:
                print(row)
```

### Pattern 3: Extract Specific Sections
```python
import pdfplumber
import re

with pdfplumber.open('specs.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()

        # Find specific sections
        if 'SECTION 200' in text:
            # Extract this section
            section_text = text
            print(section_text)
```

### Pattern 4: Convert Tables to Excel
```python
import pdfplumber
import pandas as pd

tables_data = []

with pdfplumber.open('report.pdf') as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table and len(table) > 1:
                # Convert to DataFrame
                df = pd.DataFrame(table[1:], columns=table[0])
                tables_data.append(df)

# Save all tables to Excel
with pd.ExcelWriter('extracted_tables.xlsx') as writer:
    for i, df in enumerate(tables_data):
        df.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)
```

## Construction-Specific Use Cases

### Extracting Bid Items
For bid tabulation sheets:
1. Extract tables from PDF
2. Identify columns (Item #, Description, Quantity, Unit, Price)
3. Convert to structured data (Excel/CSV)
4. Validate completeness

### Parsing Specifications
For specification documents:
1. Extract text by page or section
2. Identify CSI divisions and section numbers
3. Extract requirements, standards, and submittal requirements
4. Create searchable index

### Quantity Takeoff Support
For plan sheets with quantities:
1. Extract embedded tables
2. Look for quantity callouts
3. Extract material specifications
4. Cross-reference with specification sections

## Error Handling

Common issues and solutions:

**Empty or garbled text:**
- PDF may be scanned → Use OCR
- PDF may have security → Check permissions
- Encoding issues → Try different extraction methods

**Missing tables:**
- Table boundaries not detected → Adjust table settings
- Complex table layouts → Manual extraction may be needed
- Try different extraction libraries

**Performance issues:**
- Large PDFs → Process page by page
- Many tables → Extract tables only from relevant pages
- OCR is slow → Use only when necessary

## Best Practices

1. **Preview first** - Check a few pages manually before batch extraction
2. **Validate output** - Verify extracted data is complete and accurate
3. **Handle errors gracefully** - Some pages may fail, continue with others
4. **Save intermediate results** - Don't lose work if processing fails
5. **Document assumptions** - Note any data cleaning or transformations
6. **Preserve source info** - Track which page/PDF data came from

## Example Usage

**User Request:** "Extract the bid item list from the bid tabulation PDF and convert to Excel"

**Your Process:**
1. Open PDF and identify pages with bid tables
2. Use `extract_tables.py` to extract all tables
3. Filter for bid item tables (contain Item #, Description, Quantity, Unit, Price)
4. Convert to pandas DataFrame
5. Clean data (remove empty rows, fix formatting)
6. Export to Excel with proper column headers
7. Validate totals if present
8. Inform user of completion with file location

## Advanced Features

### OCR for Scanned Documents
```python
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ''
for i, image in enumerate(images):
    text += pytesseract.image_to_string(image)
    text += f'\n--- Page {i+1} ---\n'

print(text)
```

### Extract with Coordinates
```python
import pdfplumber

with pdfplumber.open('drawing.pdf') as pdf:
    page = pdf.pages[0]

    # Extract text with positions
    words = page.extract_words()
    for word in words:
        print(f"{word['text']} at ({word['x0']}, {word['top']})")
```

## Limitations

- **OCR accuracy** varies with scan quality
- **Complex layouts** may not extract perfectly
- **Embedded images** are not extracted as images
- **Handwritten annotations** require advanced OCR
- **Password-protected PDFs** require password
- **Form fields** may not extract completely

## Resources

- [pdfplumber documentation](https://github.com/jsvine/pdfplumber)
- [PyPDF2 documentation](https://pypdf2.readthedocs.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
