# Finance Process Skills - Setup Guide

This guide helps you set up the finance processing skills to extract and consolidate financial data.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

### Step 1: Install Required Python Packages

```bash
pip install pdfplumber pandas python-dateutil openpyxl
```

Or if you use `pip3`:

```bash
pip3 install pdfplumber pandas python-dateutil openpyxl
```

### Step 2: Verify Installation

Test the PDF extraction script:

```bash
cd .claude/skills/finance-process/extract-pdf-transactions/scripts
python3 extract_pdf_statements.py --help
```

Test the consolidation script:

```bash
cd .claude/skills/finance-process/consolidate-statements/scripts
python3 consolidate_statements.py --help
```

You should see the help text for each script if installation was successful.

## Quick Start

### Extract Transactions from PDFs

```bash
/finance-process extract \
  --input="~/Documents/Finance/*.pdf" \
  --output="~/Documents/Finance/extracted.csv"
```

### Consolidate Multiple CSV Files

```bash
/finance-process consolidate \
  --input="~/Documents/Finance/*.csv" \
  --output="~/Documents/Finance/combined.csv"
```

## Usage with Claude Code

Once installed, you can use the `/finance-process` command:

```bash
# Extract PDF statements
/finance-process extract --input="~/Documents/statements/*.pdf" --output="~/Documents/2024.csv"

# Consolidate CSV files
/finance-process consolidate --input="~/Documents/checking-*.csv" --output="~/Documents/combined.csv"

# Convert single PDF
/finance-process convert --input="~/Downloads/statement.pdf" --output="~/Documents/transactions.csv"

# Validate extracted data
/finance-process validate --input="~/Documents/transactions.csv"
```

## Troubleshooting

### "command not found: python"

Try using `python3` instead:

```bash
python3 -m pip install pdfplumber pandas python-dateutil openpyxl
```

### "ModuleNotFoundError"

Make sure all packages are installed:

```bash
pip3 install --upgrade pdfplumber pandas python-dateutil openpyxl
```

### PDF Extraction Fails

1. Check if PDF is text-based (not scanned image)
2. Verify PDF can be opened manually
3. Try different PDF library (tabula-py) as fallback
4. For scanned PDFs, OCR support may be needed (not currently implemented)

### Permission Denied

Make scripts executable:

```bash
chmod +x .claude/skills/finance-process/extract-pdf-transactions/scripts/extract_pdf_statements.py
chmod +x .claude/skills/finance-process/consolidate-statements/scripts/consolidate_statements.py
```

## Directory Structure

```
.claude/skills/finance-process/
├── README.md                           # Overview
├── SETUP.md                            # This file
├── extract-pdf-transactions/
│   ├── SKILL.md                        # Skill documentation
│   └── scripts/
│       └── extract_pdf_statements.py   # PDF extraction script
└── consolidate-statements/
    ├── SKILL.md                        # Skill documentation
    └── scripts/
        └── consolidate_statements.py   # Consolidation script
```

## Next Steps

After setup, you can:

1. Extract transactions from PDF statements
2. Consolidate multiple transaction files
3. Import consolidated data into finance notebooks
4. Analyze your financial data

See the [README.md](README.md) for detailed usage examples and workflows.
