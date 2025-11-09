# Extract PDF Transactions Skill

Extract transaction data from PDF bank and credit card statements.

## Skill Metadata

- **Name**: extract-pdf-transactions
- **Category**: Financial Data Processing
- **Complexity**: Medium
- **Privacy**: Local processing only, no external APIs

## Capabilities

This skill extracts structured transaction data from PDF financial statements:

1. **Multi-format PDF parsing** - Supports various bank statement layouts
2. **Table detection** - Automatically identifies transaction tables
3. **Data extraction** - Parses dates, descriptions, amounts, and balances
4. **Multi-page support** - Processes statements spanning multiple pages
5. **Error handling** - Gracefully handles malformed PDFs
6. **Validation** - Verifies extracted data quality

## Usage

```bash
/finance-process extract --input="~/Documents/Finance/*.pdf" --output="~/Documents/Finance/transactions.csv"
```

## How It Works

1. **PDF Discovery**: Finds all PDF files matching the input pattern
2. **Content Extraction**: Uses pdfplumber to extract text and tables
3. **Table Parsing**: Identifies transaction tables using pattern matching
4. **Data Normalization**: Standardizes column names and formats
5. **Validation**: Checks for completeness and accuracy
6. **CSV Export**: Saves transactions to specified output file

## Script

The main script is `scripts/extract_pdf_statements.py` which:
- Accepts PDF file paths (glob patterns supported)
- Extracts transaction tables
- Outputs to CSV format
- Provides progress feedback and error reporting

## Dependencies

Required Python packages:
- pdfplumber (primary extraction engine)
- pandas (data manipulation)
- python-dateutil (date parsing)
- tabula-py (fallback for complex tables)

## Output Format

The skill produces CSV files with these columns:
- `date` - Transaction date (YYYY-MM-DD)
- `description` - Transaction description/merchant
- `amount` - Transaction amount (negative for debits)
- `balance` - Account balance after transaction
- `category` - Auto-categorized transaction type
- `source_file` - Original PDF filename

## Error Handling

- Logs files that couldn't be processed
- Reports extraction quality metrics
- Provides suggestions for failed extractions
- Continues processing remaining files on error

## Privacy & Security

All PDF processing happens locally:
- No cloud API calls
- No data transmission
- Files stay on local filesystem
- Sensitive data never leaves the machine
