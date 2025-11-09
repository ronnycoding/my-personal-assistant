# Finance Process Skills

Collection of skills for processing financial documents and transaction data.

## Available Skills

### 1. extract-pdf-transactions

Extract transaction data from PDF bank and credit card statements.

**Usage:**
```bash
/finance-process extract --input="~/Documents/Finance/*.pdf" --output="transactions.csv"
```

**Script:**
```bash
cd .claude/skills/finance-process/extract-pdf-transactions/scripts
python extract_pdf_statements.py ~/Documents/Finance/*.pdf -o ~/Documents/Finance/2024.csv
```

**Features:**
- Multi-format PDF parsing
- Automatic table detection
- Date, description, and amount extraction
- Multi-page statement support
- Error handling and reporting

### 2. consolidate-statements

Combine multiple CSV/Excel transaction files into one consolidated file.

**Usage:**
```bash
/finance-process consolidate --input="~/Documents/Finance/checking-*.csv" --output="combined.csv"
```

**Script:**
```bash
cd .claude/skills/finance-process/consolidate-statements/scripts
python consolidate_statements.py ~/Documents/Finance/checking-*.csv -o ~/Documents/Finance/combined-2024.csv
```

**Features:**
- Multi-file processing
- Duplicate detection (exact and fuzzy)
- Column standardization
- Balance reconciliation
- Summary statistics

## Installation

Install required dependencies:

```bash
pip install pdfplumber pandas python-dateutil openpyxl
```

## Privacy & Security

All processing happens locally:
- No external API calls
- No cloud services
- Data stays on your local machine
- Files remain in your control

## Examples

### Extract and Consolidate Workflow

```bash
# 1. Extract transactions from PDF statements
/finance-process extract \
  --input="~/Documents/Finance/statements/*.pdf" \
  --output="~/Documents/Finance/extracted-2024.csv"

# 2. Consolidate with existing CSV files
/finance-process consolidate \
  --input="~/Documents/Finance/*.csv" \
  --output="~/Documents/Finance/all-transactions-2024.csv"

# 3. Import into finance notebook
/finance import \
  --source="~/Documents/Finance/all-transactions-2024.csv" \
  --type="combined"
```

### Direct Script Usage

```bash
# Extract PDFs
cd .claude/skills/finance-process/extract-pdf-transactions/scripts
python extract_pdf_statements.py \
  ~/Documents/Finance/*.pdf \
  -o ~/Documents/Finance/2024.csv

# Consolidate CSVs
cd .claude/skills/finance-process/consolidate-statements/scripts
python consolidate_statements.py \
  ~/Documents/Finance/checking-*.csv \
  ~/Documents/Finance/savings-*.csv \
  -o ~/Documents/Finance/combined-2024.csv
```

## Output Format

All skills produce CSV files with standardized columns:

| Column | Description |
|--------|-------------|
| date | Transaction date (YYYY-MM-DD) |
| description | Transaction description/merchant |
| amount | Transaction amount (negative for debits) |
| balance | Account balance after transaction |
| category | Transaction category (auto-categorized) |
| account | Source account (if multiple) |
| source_file | Original file name |

## Troubleshooting

### PDF Extraction Issues

If PDFs fail to extract:
1. Check if PDF is text-based (not scanned image)
2. Try opening PDF manually to verify format
3. Check error logs for specific issues
4. Some PDFs may require OCR (not yet supported)

### Consolidation Issues

If consolidation fails:
1. Verify all files are CSV or Excel format
2. Check for corrupted files
3. Ensure consistent date formats
4. Review column mappings in script

## Advanced Options

### Consolidation without deduplication

```bash
python consolidate_statements.py \
  ~/Documents/Finance/*.csv \
  -o combined.csv \
  --no-dedupe
```

### Custom duplicate tolerance

```bash
python consolidate_statements.py \
  ~/Documents/Finance/*.csv \
  -o combined.csv \
  --tolerance 5  # 5 day tolerance for fuzzy matching
```
