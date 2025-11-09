# Consolidate Statements Skill

Combine multiple CSV/Excel transaction files into a single consolidated file.

## Skill Metadata

- **Name**: consolidate-statements
- **Category**: Financial Data Processing
- **Complexity**: Low-Medium
- **Privacy**: Local processing only, no external APIs

## Capabilities

This skill consolidates transaction data from multiple files:

1. **Multi-file processing** - Handles CSV and Excel files
2. **Duplicate detection** - Removes duplicate transactions
3. **Column standardization** - Maps different column names to standard format
4. **Date sorting** - Orders transactions chronologically
5. **Balance reconciliation** - Validates running balances
6. **Summary statistics** - Provides consolidation metrics

## Usage

```bash
/finance-process consolidate --input="~/Documents/Finance/checking-*.csv" --output="~/Documents/Finance/combined-2024.csv"
```

## How It Works

1. **File Discovery**: Finds all CSV/Excel files matching the input pattern
2. **Data Loading**: Reads each file into pandas DataFrames
3. **Column Mapping**: Standardizes column names across different formats
4. **Deduplication**: Removes exact and fuzzy duplicates
5. **Sorting**: Orders transactions by date
6. **Export**: Saves consolidated data to output file

## Script

The main script is `scripts/consolidate_statements.py` which:
- Accepts CSV/Excel file paths (glob patterns supported)
- Combines all transactions
- Removes duplicates
- Standardizes format
- Outputs to CSV

## Dependencies

Required Python packages:
- pandas (data manipulation)
- openpyxl (Excel support)
- python-dateutil (date parsing)

## Output Format

The skill produces CSV files with standardized columns:
- `date` - Transaction date (YYYY-MM-DD)
- `description` - Transaction description
- `amount` - Transaction amount
- `balance` - Account balance (if available)
- `category` - Transaction category
- `account` - Source account (if multiple)
- `source_file` - Original filename

## Duplicate Detection

Duplicates are identified using:
- Exact match: Same date, description, and amount
- Fuzzy match: Similar date (±2 days) and exact amount
- Configurable tolerance levels

## Error Handling

- Reports files that couldn't be read
- Handles missing columns gracefully
- Validates data types
- Logs all operations
- Provides detailed error messages

## Privacy & Security

All file processing happens locally:
- No cloud services
- No data transmission
- Files stay on local filesystem
- Sensitive data never leaves the machine
