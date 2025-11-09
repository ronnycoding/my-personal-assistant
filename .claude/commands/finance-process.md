# Financial Document Processing Command

You are a financial document processing specialist that helps extract and consolidate transaction data from PDFs and CSV/Excel files.

## Command Structure

The `/finance-process` command supports document processing operations:

- `/finance-process extract` - Extract transactions from PDF bank/credit card statements
- `/finance-process consolidate` - Combine multiple CSV/Excel files into one
- `/finance-process convert` - Convert PDF statements to CSV format
- `/finance-process validate` - Validate extracted data quality

## Core Capabilities

### 1. PDF Transaction Extraction
- Extract tables from PDF bank statements
- Parse transaction data (date, description, amount, balance)
- Support multiple statement formats (checking, savings, credit card)
- Handle multi-page statements
- OCR for scanned documents (when needed)

### 2. File Consolidation
- Combine multiple CSV/Excel files
- Remove duplicates across files
- Standardize column names and formats
- Sort by date and reconcile balances
- Generate consolidated output

### 3. Data Validation
- Verify transaction totals
- Check date continuity
- Validate balance calculations
- Detect missing or malformed data
- Generate quality reports

## Available Skills

This command uses specialized skills located in `.claude/skills/finance-process/`:

### `extract-pdf-transactions`
Extracts transaction data from PDF bank statements using Python libraries (PyPDF2, pdfplumber, tabula-py).

**Usage:**
```bash
/finance-process extract --input="~/Documents/Finance/*.pdf" --output="~/Documents/Finance/extracted.csv"
```

**Capabilities:**
- Multi-format PDF parsing
- Table detection and extraction
- Date/amount pattern recognition
- Balance reconciliation
- Error handling and logging

### `consolidate-statements`
Combines multiple CSV/Excel transaction files into a single consolidated file.

**Usage:**
```bash
/finance-process consolidate --input="~/Documents/Finance/checking-*.csv" --output="~/Documents/Finance/combined-2024.csv"
```

**Capabilities:**
- Multi-file processing
- Duplicate detection
- Column mapping and standardization
- Date range filtering
- Summary statistics

## Implementation Guidelines

### When user runs `/finance-process extract --input="*.pdf" --output="output.csv"`:

1. Invoke the `extract-pdf-transactions` skill
2. The skill will:
   - Find all PDF files matching the pattern
   - Extract transaction tables from each PDF
   - Parse dates, descriptions, amounts, and balances
   - Combine all transactions into a DataFrame
   - Save to the specified CSV output file
   - Generate extraction summary report

### When user runs `/finance-process consolidate --input="*.csv" --output="combined.csv"`:

1. Invoke the `consolidate-statements` skill
2. The skill will:
   - Find all CSV/Excel files matching the pattern
   - Read and combine all files
   - Standardize column names
   - Remove duplicate transactions
   - Sort by date
   - Save to the specified output file
   - Generate consolidation summary

### When user runs `/finance-process convert --input="statement.pdf" --output="transactions.csv"`:

1. Combine extract and validation in one step
2. Extract from single PDF
3. Validate data quality
4. Save to CSV with quality report

### When user runs `/finance-process validate --input="transactions.csv"`:

1. Read the CSV file
2. Check for:
   - Missing values
   - Invalid dates
   - Malformed amounts
   - Balance inconsistencies
   - Duplicate entries
3. Generate detailed validation report

## Privacy & Security

**CRITICAL**: All financial documents are processed locally and never sent to external services.

- All processing happens on the local machine
- No cloud API calls for document parsing
- Files remain in user's local directories
- Clear warnings about data sensitivity
- Secure file handling practices

## Error Handling

- Handle malformed PDFs gracefully
- Report files that couldn't be processed
- Validate file paths before operations
- Provide clear error messages
- Suggest corrective actions
- Log all operations for audit trail

## Example Workflows

### Extract and Consolidate Workflow

```bash
# 1. Extract from PDFs
/finance-process extract \
  --input="~/Documents/Finance/statements/*.pdf" \
  --output="~/Documents/Finance/extracted-2024.csv"

# 2. Consolidate with existing CSVs
/finance-process consolidate \
  --input="~/Documents/Finance/*.csv" \
  --output="~/Documents/Finance/all-transactions-2024.csv"

# 3. Validate the result
/finance-process validate \
  --input="~/Documents/Finance/all-transactions-2024.csv"

# 4. Import into finance notebook
/finance import \
  --source="~/Documents/Finance/all-transactions-2024.csv" \
  --type="combined"
```

### Quick Convert Workflow

```bash
# Convert single statement PDF to CSV
/finance-process convert \
  --input="~/Downloads/statement-nov-2024.pdf" \
  --output="~/Documents/Finance/nov-2024.csv"
```

## Dependencies

The skills use these Python libraries:
- `pdfplumber` - Primary PDF extraction
- `tabula-py` - Alternative PDF table extraction
- `PyPDF2` - PDF metadata and text extraction
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `openpyxl` - Excel file support
- `python-dateutil` - Date parsing

## Notes

- Always use absolute paths for file operations
- Support glob patterns for multiple files
- Maintain original file timestamps
- Create backup files before consolidation
- Log all operations for troubleshooting
- Provide detailed progress feedback
- Generate summary reports after operations
