# Bank Statement Import Guide

Complete guide for importing bank statements into the Personal Finance Advisor.

## Quick Reference

### Location for Bank Statements

**Recommended**: `~/Documents/Finance/statements/`

```bash
mkdir -p ~/Documents/Finance/statements
mkdir -p ~/Documents/Finance/archives
```

## Scenario 1: You Have CSV/Excel Files

### Single File Import

```bash
/finance import --source="~/Documents/Finance/statements/checking-jan.csv" --type="checking"
```

### Multiple Files (Same Account)

Use the consolidation tool:

```bash
cd /Users/ronnycoding/projects/my-agents/.claude/finance-notebooks

python consolidate_statements.py \
  ~/Documents/Finance/statements/checking-*.csv \
  -o ~/Documents/Finance/combined-checking-2024.csv

# Then import the combined file
/finance import --source="~/Documents/Finance/combined-checking-2024.csv" --type="checking"
```

**Full Example:**
```bash
# You have: checking-jan.csv, checking-feb.csv, checking-mar.csv
python consolidate_statements.py \
  ~/Documents/Finance/statements/checking-{jan,feb,mar}.csv \
  -o ~/Documents/Finance/q1-checking.csv

# Output shows:
#   ✓ Loaded checking-jan.csv: 87 transactions
#   ✓ Loaded checking-feb.csv: 92 transactions
#   ✓ Loaded checking-mar.csv: 78 transactions
#   Total transactions: 257
#   Duplicates removed: 3
#   Final output: 254 transactions

/finance import --source="~/Documents/Finance/q1-checking.csv" --type="checking"
```

## Scenario 2: You Have PDF Statements

### Install PDF Tools (One-Time)

```bash
pip install pdfplumber pandas
```

### Extract from Single PDF

```bash
cd /Users/ronnycoding/projects/my-agents/.claude/finance-notebooks

python extract_pdf_statements.py \
  ~/Documents/Finance/statements/statement-jan.pdf \
  -o ~/Documents/Finance/jan-transactions.csv

# Then import
/finance import --source="~/Documents/Finance/jan-transactions.csv" --type="checking"
```

### Extract from Multiple PDFs

```bash
python extract_pdf_statements.py \
  ~/Documents/Finance/statements/*.pdf \
  -o ~/Documents/Finance/all-statements.csv

/finance import --source="~/Documents/Finance/all-statements.csv" --type="checking"
```

## Scenario 3: Multiple Accounts

Import each account separately with different `--type`:

```bash
# Checking account
/finance import --source="~/Documents/Finance/checking.csv" --type="checking"

# Savings account
/finance import --source="~/Documents/Finance/savings.csv" --type="savings"

# Credit card
/finance import --source="~/Documents/Finance/credit-card.csv" --type="credit"
```

## Complete Workflow Example

### Year-End Consolidation

```bash
# 1. Create directory structure
mkdir -p ~/Documents/Finance/2024/{checking,savings,credit}

# 2. Download all statements from your bank
#    (Usually there's a "Download all" option for the year)

# 3. If PDFs, convert them
cd /Users/ronnycoding/projects/my-agents/.claude/finance-notebooks

python extract_pdf_statements.py \
  ~/Documents/Finance/2024/checking/*.pdf \
  -o ~/Documents/Finance/2024/checking-all.csv

python extract_pdf_statements.py \
  ~/Documents/Finance/2024/savings/*.pdf \
  -o ~/Documents/Finance/2024/savings-all.csv

python extract_pdf_statements.py \
  ~/Documents/Finance/2024/credit/*.pdf \
  -o ~/Documents/Finance/2024/credit-all.csv

# 4. Create annual finance notebook
/finance init --notebook="2024-annual"

# 5. Import all accounts
/finance import --source="~/Documents/Finance/2024/checking-all.csv" --type="checking"
/finance import --source="~/Documents/Finance/2024/savings-all.csv" --type="savings"
/finance import --source="~/Documents/Finance/2024/credit-all.csv" --type="credit"

# 6. Analyze
/finance analyze --type=overview --period="2024"

# 7. Archive the source files (optional)
mv ~/Documents/Finance/2024 ~/Documents/Finance/archives/
```

## CSV Format Requirements

Your bank CSV should have these columns (column names can vary):

### Minimum Required:
- `date` (or Date, Transaction Date, Posting Date)
- `description` (or Description, Details, Merchant)
- `amount` (or Amount, Debit, Credit, Transaction Amount)

### Example CSV:
```csv
date,description,amount
2025-01-15,Grocery Store,-125.50
2025-01-16,Direct Deposit,3500.00
2025-01-17,Electric Company,-89.23
```

### Supported Date Formats:
- `2025-01-15` (YYYY-MM-DD)
- `01/15/2025` (MM/DD/YYYY)
- `15/01/2025` (DD/MM/YYYY)
- `Jan 15, 2025`
- `January 15, 2025`

## Troubleshooting

### "No columns matched the required format"

Your CSV might have different column names. Check with:
```bash
head -1 ~/Documents/Finance/statement.csv
```

Common variations handled automatically:
- Date: `Date`, `Transaction Date`, `Posting Date`
- Description: `Description`, `Details`, `Merchant`, `Payee`
- Amount: `Amount`, `Debit`, `Credit`, `Transaction Amount`

### "Invalid date format"

Some banks use non-standard formats. The tools handle most cases, but if you see errors:
1. Open CSV in Excel/Numbers
2. Ensure date column is formatted as `YYYY-MM-DD`
3. Save and retry

### "Duplicates detected"

This is normal! The import tool automatically:
- Detects exact duplicates (same date, description, amount)
- Skips transactions already in your notebook
- Reports how many were skipped

### PDF extraction found no tables

Some bank PDFs are image-based. Solutions:
1. Download CSV directly from bank (preferred)
2. Use bank's mobile app to export transactions
3. Manually transcribe to CSV (for small datasets)

## Security Best Practices

### After Import - Delete Source Files

```bash
# Import first
/finance import --source="~/Documents/Finance/statement.csv" --type="checking"

# Then delete
rm ~/Documents/Finance/statement.csv

# Or move to encrypted archive
mv ~/Documents/Finance/statement.csv ~/Documents/Finance/archives/2024/
```

### Use Encrypted Storage

**macOS:**
```bash
# Create encrypted disk image
hdiutil create -size 500m -encryption AES-256 -volname "Finance" \
  -fs APFS ~/Documents/Finance.dmg

# Mount it
open ~/Documents/Finance.dmg
# Enter password when prompted

# Now use /Volumes/Finance/ for statements
```

**Alternative - Use FileVault:**
- System Settings → Privacy & Security → FileVault
- Turn on FileVault for entire disk encryption

### Never Commit to Git

The `.gitignore` is already configured, but verify:
```bash
cd /Users/ronnycoding/projects/my-agents
git status

# Should NOT show any .csv, .xlsx, or .pdf files
# Should NOT show any .ipynb files in finance-notebooks/
```

## Tool Reference

### consolidate_statements.py

Combines multiple CSV/Excel files into one.

```bash
python consolidate_statements.py [files...] -o output.csv [--no-deduplicate]
```

Options:
- `-o, --output`: Output file path (required)
- `--no-deduplicate`: Keep duplicates (default: remove)

### extract_pdf_statements.py

Extracts transactions from PDF bank statements.

```bash
python extract_pdf_statements.py [pdf_files...] -o output.csv
```

Requirements:
- `pip install pdfplumber pandas`

Options:
- `-o, --output`: Output CSV file path

## Bank-Specific Notes

### Chase
- Download format: CSV
- Column names: `Posting Date`, `Description`, `Amount`
- ✅ Works perfectly

### Bank of America
- Download format: CSV or OFX
- Use CSV option
- Column names: `Date`, `Description`, `Amount`
- ✅ Works perfectly

### Wells Fargo
- Download format: CSV, QFX, or OFX
- Use CSV option
- ✅ Works perfectly

### Capital One
- Download format: CSV
- May include Balance column
- ✅ Works perfectly

### American Express
- Download format: CSV or OFX
- CSV has all needed columns
- ✅ Works perfectly

### Credit Unions
- Vary by institution
- Most support CSV export
- ✅ Usually works, may need column mapping

## Next Steps

After importing:

```bash
# Analyze your finances
/finance analyze --type=overview

# Create projections
/finance project --type=cashflow --months=12

# Get recommendations
/finance advise --focus="savings"

# Create visualizations
/finance report --type="income-expense"
```

## Questions?

See the [Quick Start Guide](../../../docs/finance/QUICK_START.md) for more examples.
