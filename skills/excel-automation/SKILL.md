---
name: excel-automation
description: Automate Excel operations including reading, writing, formatting, and formula manipulation
version: 1.0.0
author: Shared Agent Toolkit
tags: [excel, automation, data-processing]
---

# Excel Automation Skill

This skill provides comprehensive Excel automation capabilities using Python's openpyxl library.

## Capabilities

- **Read Excel files** - Extract data from worksheets, cells, ranges
- **Write Excel files** - Create new workbooks, add data, save files
- **Format cells** - Apply fonts, colors, borders, number formats
- **Formulas** - Insert and calculate formulas
- **Charts** - Create basic charts and graphs
- **Data validation** - Add dropdown lists and validation rules

## Prerequisites

The skill requires Python 3.7+ with the following packages:
- `openpyxl` - Excel file manipulation
- `pandas` - Data analysis and manipulation (optional but recommended)

## Usage Instructions

When a user requests Excel automation, follow this process:

### 1. Understand the Request
Clarify:
- What operation is needed (read, write, format, analyze)?
- Which file(s) are involved?
- What specific data or ranges?
- What is the desired output?

### 2. Use Helper Scripts

The `scripts/` directory contains ready-to-use utilities:

- **`excel_reader.py`** - Read data from Excel files
- **`excel_writer.py`** - Write data to new or existing files
- **`excel_formatter.py`** - Apply formatting and styles
- **`excel_formulas.py`** - Insert and calculate formulas

### 3. Execute Operations

Use the appropriate script with the user's requirements:

```bash
# Read data from a worksheet
python scripts/excel_reader.py --file "data.xlsx" --sheet "Sheet1" --range "A1:D10"

# Write data to Excel
python scripts/excel_writer.py --file "output.xlsx" --data "data.json"

# Format cells
python scripts/excel_formatter.py --file "report.xlsx" --format-header
```

### 4. Provide Results

- Show the user what was accomplished
- Provide file paths for generated files
- Explain any data transformations
- Suggest next steps if applicable

## Common Patterns

### Pattern 1: Read and Analyze
```python
import openpyxl

# Load workbook
wb = openpyxl.load_workbook('data.xlsx')
ws = wb['Sheet1']

# Read data
data = []
for row in ws.iter_rows(min_row=2, values_only=True):
    data.append(row)

# Analyze
print(f"Total rows: {len(data)}")
```

### Pattern 2: Create Report
```python
import openpyxl
from openpyxl.styles import Font, Alignment

# Create workbook
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Report"

# Add header
ws['A1'] = "Report Title"
ws['A1'].font = Font(size=14, bold=True)
ws['A1'].alignment = Alignment(horizontal='center')

# Add data
data = [["Name", "Value"], ["Item 1", 100], ["Item 2", 200]]
for row in data:
    ws.append(row)

wb.save('report.xlsx')
```

### Pattern 3: Formulas and Calculations
```python
import openpyxl

wb = openpyxl.load_workbook('budget.xlsx')
ws = wb['Budget']

# Add SUM formula
ws['D10'] = '=SUM(D2:D9)'

# Add formula for each row
for row in range(2, 10):
    ws[f'E{row}'] = f'=C{row}*D{row}'

wb.save('budget.xlsx')
```

## Error Handling

Always handle common errors:
- File not found
- Sheet doesn't exist
- Invalid cell reference
- Permission denied (file open in Excel)
- Data type mismatches

## Best Practices

1. **Backup files** before modifying existing workbooks
2. **Validate input** - check file exists, sheet names are correct
3. **Close files properly** - ensure workbooks are saved and closed
4. **Use data_only=True** when reading calculated values
5. **Consider memory** - for large files, use `read_only=True`

## Example Usage

**User Request:** "Read the quarterly sales data from Q4_Sales.xlsx and create a summary report"

**Your Response:**
1. Read the data using `excel_reader.py`
2. Analyze the data (calculate totals, averages)
3. Create a new formatted summary report
4. Save as "Q4_Sales_Summary.xlsx"
5. Inform user of completion with file location

## Limitations

- Very large files (>100MB) may be slow
- Complex formatting may not be preserved perfectly
- Charts are basic - complex charts may require manual creation
- Macros (VBA) are not supported

## Resources

- [openpyxl documentation](https://openpyxl.readthedocs.io/)
- [Excel formula reference](https://support.microsoft.com/en-us/excel)
