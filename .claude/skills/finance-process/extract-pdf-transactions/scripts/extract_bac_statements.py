#!/usr/bin/env python3
"""
Extract transactions from BAC bank PDF statements (Costa Rica format).

Usage:
    python extract_bac_statements.py <pdf_files> -o <output.csv>

Example:
    python extract_bac_statements.py ~/Documents/Finance/2025/*.pdf -o transactions.csv
"""

import argparse
import glob
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import sys

try:
    import pdfplumber
    import pandas as pd
except ImportError as e:
    print(f"ERROR: Missing required package: {e}")
    print("\nInstall dependencies with:")
    print("  pip install pdfplumber pandas")
    sys.exit(1)


class BACStatementExtractor:
    """Extract transaction data from BAC bank PDF statements."""

    # Month name mapping (Spanish to number)
    MONTHS = {
        'ENE': 1, 'FEB': 2, 'MAR': 3, 'ABR': 4, 'MAY': 5, 'JUN': 6,
        'JUL': 7, 'AGO': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DIC': 12
    }

    def __init__(self):
        self.transactions = []
        self.errors = []
        self.stats = {
            'files_processed': 0,
            'files_failed': 0,
            'transactions_found': 0
        }

    def extract_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract transactions from a single BAC PDF file."""
        print(f"Processing: {Path(pdf_path).name}")

        try:
            # Determine currency and statement month from filename
            filename = Path(pdf_path).stem
            currency = self._detect_currency(filename)
            statement_month = self._extract_statement_month(filename)

            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        self._parse_transactions(text, pdf_path, currency, statement_month)

            self.stats['files_processed'] += 1
            print(f"  ✓ Extracted {self.stats['transactions_found']} transactions")

        except Exception as e:
            error_msg = f"Failed to process {pdf_path}: {str(e)}"
            print(f"  ✗ {error_msg}")
            self.errors.append(error_msg)
            self.stats['files_failed'] += 1

        return self.transactions

    def _detect_currency(self, filename: str) -> str:
        """Detect currency from filename."""
        if '_USD_' in filename:
            return 'USD'
        elif '_CRC_' in filename:
            return 'CRC'
        return 'UNKNOWN'

    def _extract_statement_month(self, filename: str) -> str:
        """Extract statement month from filename."""
        for month_abbr in self.MONTHS.keys():
            if month_abbr in filename:
                return month_abbr
        return None

    def _parse_transactions(self, text: str, source_file: str, currency: str, statement_month: str):
        """Parse transactions from PDF text."""
        lines = text.split('\n')

        # Look for transaction lines
        # Format: REFERENCE_NUM MONTH/DAY DESCRIPTION AMOUNT
        # Example: 090100248 SEP/01 BAR ASTRO BOY 7,500.00

        transaction_pattern = re.compile(
            r'^\s*(\d+)\s+([A-Z]{3})/(\d{1,2})\s+(.*?)\s+([\d,]+\.\d{2})\s*$'
        )

        for line in lines:
            match = transaction_pattern.match(line)
            if match:
                ref_num = match.group(1)
                month_abbr = match.group(2)
                day = match.group(3)
                description = match.group(4).strip()
                amount_str = match.group(5)

                # Parse amount
                amount = float(amount_str.replace(',', ''))

                # Construct date
                date_obj = self._construct_date(month_abbr, day, statement_month)

                transaction = {
                    'date': date_obj.strftime('%Y-%m-%d') if date_obj else None,
                    'description': description,
                    'reference': ref_num,
                    'amount': -amount,  # Debits are negative
                    'currency': currency,
                    'source_file': Path(source_file).name
                }

                self.transactions.append(transaction)
                self.stats['transactions_found'] += 1

    def _construct_date(self, month_abbr: str, day: str, statement_month: str) -> datetime:
        """Construct date from month abbreviation and day."""
        try:
            month_num = self.MONTHS.get(month_abbr)
            if not month_num:
                return None

            # Determine year based on statement month
            # If transaction is from previous month at end of statement, use previous year logic
            current_year = datetime.now().year

            # For 2025 statements, use 2025 as base year
            # Adjust if transaction month is after statement month (wrapped to previous year)
            statement_month_num = self.MONTHS.get(statement_month) if statement_month else month_num

            if month_num > statement_month_num:
                # Transaction from previous year
                year = current_year - 1
            else:
                year = current_year

            day_num = int(day)
            return datetime(year, month_num, day_num)

        except (ValueError, TypeError):
            return None

    def to_dataframe(self) -> pd.DataFrame:
        """Convert transactions to pandas DataFrame."""
        if not self.transactions:
            return pd.DataFrame()

        df = pd.DataFrame(self.transactions)

        # Ensure required columns exist
        for col in ['date', 'description', 'amount', 'currency', 'reference', 'source_file']:
            if col not in df.columns:
                df[col] = None

        # Sort by date
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.sort_values('date')

        # Add category column
        df['category'] = 'Uncategorized'

        return df[['date', 'description', 'amount', 'currency', 'reference', 'category', 'source_file']]


def main():
    parser = argparse.ArgumentParser(description='Extract transactions from BAC bank PDF statements')
    parser.add_argument('pdf_files', nargs='+', help='PDF files to process (supports glob patterns)')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file')

    args = parser.parse_args()

    # Expand glob patterns
    pdf_files = []
    for pattern in args.pdf_files:
        expanded = glob.glob(pattern)
        if expanded:
            pdf_files.extend(expanded)
        else:
            pdf_files.append(pattern)

    # Filter for PDF files
    pdf_files = [f for f in pdf_files if f.lower().endswith('.pdf')]

    if not pdf_files:
        print("ERROR: No PDF files found")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  BAC Bank Statement Extractor")
    print(f"{'='*60}\n")
    print(f"Found {len(pdf_files)} PDF file(s) to process\n")

    # Extract transactions
    extractor = BACStatementExtractor()

    for pdf_file in pdf_files:
        extractor.extract_from_pdf(pdf_file)

    # Convert to DataFrame and save
    df = extractor.to_dataframe()

    if df.empty:
        print("\n✗ No transactions extracted")
        if extractor.errors:
            print("\nErrors encountered:")
            for error in extractor.errors:
                print(f"  - {error}")
        sys.exit(1)

    # Save to CSV
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    # Summary
    print(f"\n{'='*60}")
    print(f"  Extraction Complete")
    print(f"{'='*60}")
    print(f"Files processed: {extractor.stats['files_processed']}")
    print(f"Total transactions: {len(df)}")

    if not df.empty:
        print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")

        # Group by currency
        if 'currency' in df.columns:
            print(f"\nBy currency:")
            for curr in df['currency'].unique():
                curr_df = df[df['currency'] == curr]
                total = curr_df['amount'].sum()
                count = len(curr_df)
                print(f"  {curr}: {count} transactions, Total: {total:,.2f}")

    if extractor.errors:
        print(f"\nWarnings: {len(extractor.errors)} file(s) had errors")

    print(f"\n✓ Successfully extracted to {output_path}\n")


if __name__ == '__main__':
    main()
