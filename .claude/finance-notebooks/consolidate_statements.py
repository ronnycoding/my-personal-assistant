#!/usr/bin/env python3
"""
Bank Statement Consolidation Tool

Combines multiple CSV/Excel bank statements into a single file for import.
Handles duplicate removal, date sorting, and format standardization.

Usage:
    python consolidate_statements.py ~/Documents/Finance/statements/*.csv -o combined.csv
    python consolidate_statements.py ~/Documents/Finance/statements/*.xlsx -o combined.csv
"""

import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime
import sys


def consolidate_statements(input_files, output_file, deduplicate=True):
    """
    Consolidate multiple bank statement files into one.

    Args:
        input_files: List of file paths (CSV or Excel)
        output_file: Output file path
        deduplicate: Remove duplicate transactions (default: True)

    Returns:
        Number of transactions in final file
    """
    print(f"📄 Consolidating {len(input_files)} statement files...")

    all_transactions = []

    for file_path in input_files:
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"⚠️  Skipping {file_path.name}: File not found")
            continue

        try:
            # Read file based on extension
            if file_path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                print(f"⚠️  Skipping {file_path.name}: Unsupported format")
                continue

            print(f"  ✓ Loaded {file_path.name}: {len(df)} transactions")
            all_transactions.append(df)

        except Exception as e:
            print(f"  ✗ Error loading {file_path.name}: {e}")
            continue

    if not all_transactions:
        print("❌ No valid statements found!")
        return 0

    # Combine all DataFrames
    print("\n🔄 Combining transactions...")
    combined = pd.concat(all_transactions, ignore_index=True)
    print(f"  Total transactions before processing: {len(combined)}")

    # Standardize column names (common variations)
    column_mappings = {
        'Date': 'date',
        'DATE': 'date',
        'Transaction Date': 'date',
        'Posting Date': 'date',
        'Description': 'description',
        'DESCRIPTION': 'description',
        'Details': 'description',
        'Merchant': 'description',
        'Amount': 'amount',
        'AMOUNT': 'amount',
        'Transaction Amount': 'amount',
        'Debit': 'amount',
        'Credit': 'amount',
    }

    combined.rename(columns=column_mappings, inplace=True)

    # Ensure required columns exist
    required_columns = ['date', 'description', 'amount']
    missing_columns = [col for col in required_columns if col not in combined.columns]

    if missing_columns:
        print(f"❌ Missing required columns: {missing_columns}")
        print(f"Available columns: {list(combined.columns)}")
        return 0

    # Convert date to datetime
    print("\n📅 Parsing dates...")
    combined['date'] = pd.to_datetime(combined['date'], errors='coerce')

    # Remove rows with invalid dates
    invalid_dates = combined['date'].isna().sum()
    if invalid_dates > 0:
        print(f"  ⚠️  Removing {invalid_dates} transactions with invalid dates")
        combined = combined.dropna(subset=['date'])

    # Convert amount to numeric
    print("\n💵 Parsing amounts...")
    if not pd.api.types.is_numeric_dtype(combined['amount']):
        # Remove currency symbols and commas
        combined['amount'] = combined['amount'].astype(str).str.replace('[$,]', '', regex=True)
        combined['amount'] = pd.to_numeric(combined['amount'], errors='coerce')

    # Remove rows with invalid amounts
    invalid_amounts = combined['amount'].isna().sum()
    if invalid_amounts > 0:
        print(f"  ⚠️  Removing {invalid_amounts} transactions with invalid amounts")
        combined = combined.dropna(subset=['amount'])

    # Remove zero amounts
    zero_amounts = (combined['amount'] == 0).sum()
    if zero_amounts > 0:
        print(f"  ⚠️  Removing {zero_amounts} transactions with zero amount")
        combined = combined[combined['amount'] != 0]

    # Sort by date
    print("\n🔀 Sorting by date...")
    combined = combined.sort_values('date').reset_index(drop=True)

    # Deduplicate if requested
    if deduplicate:
        print("\n🔍 Removing duplicates...")
        before_dedup = len(combined)
        combined = combined.drop_duplicates(subset=['date', 'description', 'amount'])
        duplicates_removed = before_dedup - len(combined)
        print(f"  Removed {duplicates_removed} duplicate transactions")

    # Keep only essential columns (and any extra columns that exist)
    output_columns = ['date', 'description', 'amount']
    optional_columns = ['category', 'account', 'type', 'balance']
    for col in optional_columns:
        if col in combined.columns:
            output_columns.append(col)

    combined = combined[output_columns]

    # Save to file
    print(f"\n💾 Saving to {output_file}...")
    output_path = Path(output_file)

    if output_path.suffix.lower() == '.csv':
        combined.to_csv(output_path, index=False)
    elif output_path.suffix.lower() in ['.xlsx', '.xls']:
        combined.to_excel(output_path, index=False)
    else:
        # Default to CSV
        output_path = output_path.with_suffix('.csv')
        combined.to_csv(output_path, index=False)

    # Summary
    print("\n" + "="*60)
    print("✅ Consolidation Complete!")
    print("="*60)
    print(f"Output file: {output_path}")
    print(f"Total transactions: {len(combined)}")
    print(f"Date range: {combined['date'].min().strftime('%Y-%m-%d')} to {combined['date'].max().strftime('%Y-%m-%d')}")
    print(f"Total amount: ${combined['amount'].sum():,.2f}")
    print()
    print("Next steps:")
    print(f"  /finance import --source=\"{output_path}\" --type=\"checking\"")
    print()

    return len(combined)


def main():
    parser = argparse.ArgumentParser(
        description='Consolidate multiple bank statement files into one',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Consolidate all CSV files in a directory
  python consolidate_statements.py ~/Documents/Finance/*.csv -o combined.csv

  # Consolidate specific files
  python consolidate_statements.py checking-jan.csv checking-feb.csv -o q1-checking.csv

  # Include Excel files
  python consolidate_statements.py statements/*.xlsx -o all-2024.csv

  # Keep duplicates (no deduplication)
  python consolidate_statements.py *.csv -o combined.csv --no-deduplicate
        """
    )

    parser.add_argument(
        'input_files',
        nargs='+',
        help='Input statement files (CSV or Excel)'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output file path'
    )

    parser.add_argument(
        '--no-deduplicate',
        action='store_false',
        dest='deduplicate',
        help='Keep duplicate transactions (default: remove duplicates)'
    )

    args = parser.parse_args()

    # Expand file paths
    input_files = [Path(f).expanduser() for f in args.input_files]
    output_file = Path(args.output).expanduser()

    # Consolidate
    count = consolidate_statements(input_files, output_file, args.deduplicate)

    if count == 0:
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
