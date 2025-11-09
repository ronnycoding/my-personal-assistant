#!/usr/bin/env python3
"""
Consolidate multiple CSV/Excel transaction files into one.

Usage:
    python consolidate_statements.py <files> -o <output.csv>

Example:
    python consolidate_statements.py ~/Documents/Finance/*.csv -o combined.csv
"""

import argparse
import glob
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"ERROR: Missing required package: {e}")
    print("\nInstall dependencies with:")
    print("  pip install pandas openpyxl")
    sys.exit(1)


class StatementConsolidator:
    """Consolidate multiple transaction files."""

    # Common column name variations
    COLUMN_MAPPINGS = {
        'date': ['date', 'transaction date', 'trans date', 'post date', 'posting date'],
        'description': ['description', 'merchant', 'desc', 'memo', 'details', 'payee'],
        'amount': ['amount', 'transaction amount', 'debit', 'credit', 'value'],
        'balance': ['balance', 'running balance', 'account balance', 'ending balance'],
        'category': ['category', 'type', 'transaction type', 'class'],
        'account': ['account', 'account name', 'account number'],
    }

    def __init__(self, dedupe: bool = True, tolerance_days: int = 2):
        self.all_transactions = []
        self.dedupe = dedupe
        self.tolerance_days = tolerance_days
        self.errors = []
        self.stats = {
            'files_processed': 0,
            'files_failed': 0,
            'total_rows': 0,
            'duplicates_removed': 0,
        }

    def consolidate_files(self, file_paths: List[str]) -> pd.DataFrame:
        """Consolidate multiple transaction files."""
        print(f"\n{'='*60}")
        print(f"  Statement Consolidator")
        print(f"{'='*60}\n")

        for file_path in file_paths:
            self._process_file(file_path)

        if not self.all_transactions:
            print("\n✗ No transactions loaded")
            return pd.DataFrame()

        # Combine all DataFrames
        df = pd.concat(self.all_transactions, ignore_index=True)
        self.stats['total_rows'] = len(df)

        print(f"\nCombined {len(df)} transactions from {self.stats['files_processed']} files")

        # Standardize and clean
        df = self._standardize_dataframe(df)

        # Remove duplicates if enabled
        if self.dedupe:
            original_count = len(df)
            df = self._remove_duplicates(df)
            self.stats['duplicates_removed'] = original_count - len(df)
            print(f"Removed {self.stats['duplicates_removed']} duplicate transactions")

        # Sort by date
        if 'date' in df.columns:
            df = df.sort_values('date').reset_index(drop=True)

        return df

    def _process_file(self, file_path: str):
        """Process a single file."""
        print(f"Processing: {file_path}")

        try:
            # Read file based on extension
            file_path_obj = Path(file_path)
            if file_path_obj.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif file_path_obj.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
            else:
                print(f"  ✗ Unsupported file type: {file_path_obj.suffix}")
                self.stats['files_failed'] += 1
                return

            if df.empty:
                print(f"  ⚠ File is empty")
                return

            # Add source file metadata
            df['source_file'] = file_path_obj.name

            # Map columns to standard names
            df = self._map_columns(df)

            self.all_transactions.append(df)
            self.stats['files_processed'] += 1
            print(f"  ✓ Loaded {len(df)} transactions")

        except Exception as e:
            error_msg = f"Failed to process {file_path}: {str(e)}"
            print(f"  ✗ {error_msg}")
            self.errors.append(error_msg)
            self.stats['files_failed'] += 1

    def _map_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Map columns to standard names."""
        column_map = {}

        # Try to map each standard column
        for standard_name, variations in self.COLUMN_MAPPINGS.items():
            for col in df.columns:
                if col.lower().strip() in [v.lower() for v in variations]:
                    column_map[col] = standard_name
                    break

        # Rename columns
        if column_map:
            df = df.rename(columns=column_map)

        return df

    def _standardize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize DataFrame format."""
        # Ensure required columns exist
        for col in ['date', 'description', 'amount']:
            if col not in df.columns:
                print(f"⚠ Warning: '{col}' column not found")
                df[col] = None

        # Parse dates
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Standardize amounts
        if 'amount' in df.columns:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

        # Handle balance column
        if 'balance' in df.columns:
            df['balance'] = pd.to_numeric(df['balance'], errors='coerce')
        else:
            df['balance'] = None

        # Ensure other standard columns exist
        for col in ['category', 'account']:
            if col not in df.columns:
                df[col] = None

        # Select and order columns
        output_columns = ['date', 'description', 'amount', 'balance', 'category', 'account', 'source_file']
        for col in output_columns:
            if col not in df.columns:
                df[col] = None

        return df[output_columns]

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate transactions."""
        if df.empty:
            return df

        # Method 1: Exact duplicates
        # Keep first occurrence based on date, description, amount
        subset_cols = ['date', 'description', 'amount']
        available_cols = [col for col in subset_cols if col in df.columns and df[col].notna().any()]

        if available_cols:
            df = df.drop_duplicates(subset=available_cols, keep='first')

        # Method 2: Fuzzy duplicates (same amount, similar date)
        if 'date' in df.columns and 'amount' in df.columns:
            df = self._remove_fuzzy_duplicates(df)

        return df

    def _remove_fuzzy_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove fuzzy duplicates (similar date, exact amount)."""
        to_drop = set()

        # Sort by date and amount
        df_sorted = df.sort_values(['date', 'amount']).reset_index()

        for i in range(len(df_sorted) - 1):
            if i in to_drop:
                continue

            row_i = df_sorted.iloc[i]

            # Look ahead for potential duplicates
            for j in range(i + 1, len(df_sorted)):
                if j in to_drop:
                    continue

                row_j = df_sorted.iloc[j]

                # Check if amounts match exactly
                if abs(row_i['amount'] - row_j['amount']) < 0.01:
                    # Check if dates are within tolerance
                    date_diff = abs((row_i['date'] - row_j['date']).days)
                    if date_diff <= self.tolerance_days:
                        # Mark as duplicate
                        to_drop.add(j)
                else:
                    # If amounts don't match, no point looking further
                    break

        # Drop fuzzy duplicates
        if to_drop:
            df_sorted = df_sorted.drop(list(to_drop))
            df = df_sorted.drop(columns=['index']).reset_index(drop=True)

        return df

    def print_summary(self, df: pd.DataFrame):
        """Print consolidation summary."""
        print(f"\n{'='*60}")
        print(f"  Consolidation Summary")
        print(f"{'='*60}")
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Files failed: {self.stats['files_failed']}")
        print(f"Total transactions: {len(df)}")
        print(f"Duplicates removed: {self.stats['duplicates_removed']}")

        if not df.empty and 'date' in df.columns:
            date_range = f"{df['date'].min().date()} to {df['date'].max().date()}"
            print(f"Date range: {date_range}")

        if not df.empty and 'amount' in df.columns:
            total = df['amount'].sum()
            print(f"Total amount: ${total:,.2f}")

        if not df.empty and 'source_file' in df.columns:
            print(f"\nSource files:")
            for source in df['source_file'].unique():
                count = len(df[df['source_file'] == source])
                print(f"  - {source}: {count} transactions")

        if self.errors:
            print(f"\n⚠ Warnings: {len(self.errors)} error(s)")
            for error in self.errors[:5]:  # Show first 5 errors
                print(f"  - {error}")

        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='Consolidate multiple transaction files')
    parser.add_argument('files', nargs='+', help='Files to consolidate (supports glob patterns)')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file')
    parser.add_argument('--no-dedupe', action='store_true', help='Disable duplicate removal')
    parser.add_argument('--tolerance', type=int, default=2,
                        help='Days tolerance for fuzzy duplicate detection (default: 2)')

    args = parser.parse_args()

    # Expand glob patterns
    all_files = []
    for pattern in args.files:
        expanded = glob.glob(pattern)
        if expanded:
            all_files.extend(expanded)
        else:
            all_files.append(pattern)

    # Filter for supported files
    supported_extensions = ['.csv', '.xlsx', '.xls']
    input_files = [f for f in all_files if Path(f).suffix.lower() in supported_extensions]

    if not input_files:
        print("ERROR: No CSV/Excel files found")
        sys.exit(1)

    print(f"Found {len(input_files)} file(s) to consolidate")

    # Consolidate
    consolidator = StatementConsolidator(
        dedupe=not args.no_dedupe,
        tolerance_days=args.tolerance
    )

    df = consolidator.consolidate_files(input_files)

    if df.empty:
        print("\n✗ No transactions to save")
        sys.exit(1)

    # Save output
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    # Print summary
    consolidator.print_summary(df)

    print(f"✓ Successfully consolidated to {output_path}\n")


if __name__ == '__main__':
    main()
