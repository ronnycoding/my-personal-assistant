#!/usr/bin/env python3
"""
PDF Bank Statement Extraction Tool

Extracts transaction tables from PDF bank statements and converts to CSV.
Uses pdfplumber for robust table extraction.

Installation:
    pip install pdfplumber pandas

Usage:
    python extract_pdf_statements.py statement.pdf -o transactions.csv
    python extract_pdf_statements.py statements/*.pdf -o combined.csv
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

try:
    import pdfplumber
except ImportError:
    print("❌ pdfplumber not installed!")
    print("Install with: pip install pdfplumber")
    sys.exit(1)


def extract_transactions_from_pdf(pdf_path, output_path=None):
    """
    Extract transaction table from PDF bank statement.

    Args:
        pdf_path: Path to PDF file
        output_path: Optional output CSV path

    Returns:
        DataFrame with transactions
    """
    print(f"\n📄 Processing: {pdf_path.name}")

    all_transactions = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"  Pages: {len(pdf.pages)}")

            for page_num, page in enumerate(pdf.pages, 1):
                print(f"  Extracting page {page_num}...", end=" ")

                # Extract tables from page
                tables = page.extract_tables()

                if not tables:
                    print("(no tables)")
                    continue

                print(f"({len(tables)} tables)")

                for table_num, table in enumerate(tables, 1):
                    if not table or len(table) < 2:  # Need header + at least 1 row
                        continue

                    # Convert table to DataFrame
                    df = pd.DataFrame(table[1:], columns=table[0])

                    # Try to identify transaction columns
                    # Common patterns: Date, Description/Details, Amount/Debit/Credit
                    date_cols = [col for col in df.columns if col and any(
                        keyword in str(col).lower()
                        for keyword in ['date', 'trans', 'post']
                    )]

                    desc_cols = [col for col in df.columns if col and any(
                        keyword in str(col).lower()
                        for keyword in ['description', 'details', 'merchant', 'payee']
                    )]

                    amount_cols = [col for col in df.columns if col and any(
                        keyword in str(col).lower()
                        for keyword in ['amount', 'debit', 'credit', 'withdrawal', 'deposit']
                    )]

                    if not (date_cols and desc_cols and amount_cols):
                        print(f"    Table {table_num}: Skipped (not transaction table)")
                        continue

                    print(f"    Table {table_num}: {len(df)} rows extracted")

                    # Standardize column names
                    rename_map = {}
                    if date_cols:
                        rename_map[date_cols[0]] = 'date'
                    if desc_cols:
                        rename_map[desc_cols[0]] = 'description'
                    if amount_cols:
                        rename_map[amount_cols[0]] = 'amount'

                    df = df.rename(columns=rename_map)

                    # Keep only essential columns
                    essential_cols = ['date', 'description', 'amount']
                    available_cols = [col for col in essential_cols if col in df.columns]
                    df = df[available_cols]

                    # Remove empty rows
                    df = df.dropna(how='all')

                    all_transactions.append(df)

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

    if not all_transactions:
        print(f"  ⚠️  No transaction tables found in {pdf_path.name}")
        return None

    # Combine all extracted tables
    combined = pd.concat(all_transactions, ignore_index=True)

    print(f"  ✓ Extracted {len(combined)} total transactions")

    # Clean up data
    print(f"  🧹 Cleaning data...")

    # Remove rows where all essential fields are empty
    combined = combined.dropna(subset=['date', 'description', 'amount'], how='all')

    # Clean amount column (remove $, commas, parentheses for negative)
    if 'amount' in combined.columns:
        combined['amount'] = combined['amount'].astype(str)

        # Handle parentheses for negative amounts (accounting format)
        combined['amount'] = combined['amount'].str.replace(r'^\((.*)\)$', r'-\1', regex=True)

        # Remove currency symbols and commas
        combined['amount'] = combined['amount'].str.replace(r'[$,]', '', regex=True)

        # Convert to numeric
        combined['amount'] = pd.to_numeric(combined['amount'], errors='coerce')

    # Parse dates
    if 'date' in combined.columns:
        combined['date'] = pd.to_datetime(combined['date'], errors='coerce')

    # Remove invalid rows
    combined = combined.dropna(subset=['date', 'amount'])

    # Sort by date
    combined = combined.sort_values('date').reset_index(drop=True)

    print(f"  ✓ {len(combined)} valid transactions after cleaning")

    # Save if output path provided
    if output_path:
        combined.to_csv(output_path, index=False)
        print(f"  💾 Saved to: {output_path}")

    return combined


def main():
    parser = argparse.ArgumentParser(
        description='Extract transactions from PDF bank statements',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from single PDF
  python extract_pdf_statements.py statement-jan.pdf -o jan-transactions.csv

  # Extract from multiple PDFs and combine
  python extract_pdf_statements.py statements/*.pdf -o all-2024.csv

  # Preview extraction without saving
  python extract_pdf_statements.py statement.pdf

Requirements:
  pip install pdfplumber pandas
        """
    )

    parser.add_argument(
        'pdf_files',
        nargs='+',
        help='PDF bank statement files'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output CSV file path'
    )

    args = parser.parse_args()

    # Process each PDF
    all_dfs = []

    for pdf_file in args.pdf_files:
        pdf_path = Path(pdf_file).expanduser()

        if not pdf_path.exists():
            print(f"⚠️  Skipping {pdf_path}: File not found")
            continue

        if pdf_path.suffix.lower() != '.pdf':
            print(f"⚠️  Skipping {pdf_path}: Not a PDF file")
            continue

        df = extract_transactions_from_pdf(pdf_path)
        if df is not None and len(df) > 0:
            all_dfs.append(df)

    if not all_dfs:
        print("\n❌ No transactions extracted from any PDF!")
        sys.exit(1)

    # Combine all extractions
    print("\n" + "="*60)
    print("📊 Consolidating All Extractions")
    print("="*60)

    combined = pd.concat(all_dfs, ignore_index=True)

    # Remove duplicates
    before_dedup = len(combined)
    combined = combined.drop_duplicates(subset=['date', 'description', 'amount'])
    duplicates = before_dedup - len(combined)

    print(f"Total transactions: {len(combined)}")
    if duplicates > 0:
        print(f"Duplicates removed: {duplicates}")

    if len(combined) > 0:
        print(f"Date range: {combined['date'].min().strftime('%Y-%m-%d')} to {combined['date'].max().strftime('%Y-%m-%d')}")
        print(f"Total amount: ${combined['amount'].sum():,.2f}")

    # Save if output specified
    if args.output:
        output_path = Path(args.output).expanduser()
        combined.to_csv(output_path, index=False)

        print("\n" + "="*60)
        print("✅ Extraction Complete!")
        print("="*60)
        print(f"Output file: {output_path}")
        print(f"Transactions: {len(combined)}")
        print()
        print("Next steps:")
        print(f'  /finance import --source="{output_path}" --type="checking"')
        print()
    else:
        print("\n💡 Tip: Use -o to save to CSV file")
        print("\nPreview of extracted data:")
        print(combined.head(10).to_string())

    sys.exit(0)


if __name__ == '__main__':
    main()
