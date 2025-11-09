#!/usr/bin/env python3
"""
Extract transactions from PDF bank statements.

Usage:
    python extract_pdf_statements.py <pdf_files> -o <output.csv>

Example:
    python extract_pdf_statements.py ~/Documents/Finance/*.pdf -o transactions.csv
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
    from dateutil import parser as date_parser
except ImportError as e:
    print(f"ERROR: Missing required package: {e}")
    print("\nInstall dependencies with:")
    print("  pip install pdfplumber pandas python-dateutil")
    sys.exit(1)


class PDFStatementExtractor:
    """Extract transaction data from PDF bank statements."""

    # Common date patterns
    DATE_PATTERNS = [
        r'\d{1,2}/\d{1,2}/\d{2,4}',  # MM/DD/YYYY or M/D/YY
        r'\d{1,2}-\d{1,2}-\d{2,4}',  # MM-DD-YYYY
        r'\d{4}-\d{2}-\d{2}',        # YYYY-MM-DD
    ]

    # Amount patterns (including negative)
    AMOUNT_PATTERN = r'-?\$?\d{1,3}(?:,\d{3})*(?:\.\d{2})?'

    def __init__(self):
        self.transactions = []
        self.errors = []

    def extract_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract transactions from a single PDF file."""
        print(f"Processing: {pdf_path}")

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    print(f"  Page {page_num}/{len(pdf.pages)}", end='\r')

                    # Try table extraction first
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            self._process_table(table, pdf_path)

                    # Fallback to text extraction
                    else:
                        text = page.extract_text()
                        if text:
                            self._process_text(text, pdf_path)

                print(f"  ✓ Extracted {len(self.transactions)} transactions")

        except Exception as e:
            error_msg = f"Failed to process {pdf_path}: {str(e)}"
            print(f"  ✗ {error_msg}")
            self.errors.append(error_msg)

        return self.transactions

    def _process_table(self, table: List[List[str]], source_file: str):
        """Process a table extracted from PDF."""
        if not table or len(table) < 2:
            return

        # Try to identify columns
        header = table[0]
        date_col = self._find_column(header, ['date', 'trans date', 'post date'])
        desc_col = self._find_column(header, ['description', 'merchant', 'desc'])
        amount_col = self._find_column(header, ['amount', 'debit', 'credit'])
        balance_col = self._find_column(header, ['balance', 'running balance'])

        # Process rows
        for row in table[1:]:
            if len(row) < 2:
                continue

            try:
                transaction = {}

                # Extract date
                if date_col is not None and date_col < len(row):
                    date_str = row[date_col]
                    transaction['date'] = self._parse_date(date_str)
                else:
                    # Try to find date in any column
                    for cell in row:
                        if self._looks_like_date(cell):
                            transaction['date'] = self._parse_date(cell)
                            break

                # Extract description
                if desc_col is not None and desc_col < len(row):
                    transaction['description'] = row[desc_col].strip()
                else:
                    # Use first non-date, non-amount column
                    for cell in row:
                        if cell and not self._looks_like_date(cell) and not self._looks_like_amount(cell):
                            transaction['description'] = cell.strip()
                            break

                # Extract amount
                if amount_col is not None and amount_col < len(row):
                    amount_str = row[amount_col]
                    transaction['amount'] = self._parse_amount(amount_str)
                else:
                    # Try to find amount in any column
                    for cell in row:
                        if self._looks_like_amount(cell):
                            transaction['amount'] = self._parse_amount(cell)
                            break

                # Extract balance
                if balance_col is not None and balance_col < len(row):
                    balance_str = row[balance_col]
                    transaction['balance'] = self._parse_amount(balance_str)

                # Add metadata
                transaction['source_file'] = Path(source_file).name

                # Only add if we have minimum required fields
                if 'date' in transaction and 'amount' in transaction:
                    self.transactions.append(transaction)

            except Exception as e:
                # Skip malformed rows
                continue

    def _process_text(self, text: str, source_file: str):
        """Process raw text when table extraction fails."""
        lines = text.split('\n')

        for line in lines:
            # Look for lines with date and amount pattern
            if self._looks_like_transaction_line(line):
                try:
                    transaction = self._parse_transaction_line(line)
                    if transaction:
                        transaction['source_file'] = Path(source_file).name
                        self.transactions.append(transaction)
                except Exception:
                    continue

    def _find_column(self, header: List[str], keywords: List[str]) -> int:
        """Find column index by matching keywords."""
        for i, col in enumerate(header):
            if col and any(kw.lower() in col.lower() for kw in keywords):
                return i
        return None

    def _looks_like_date(self, text: str) -> bool:
        """Check if text looks like a date."""
        if not text:
            return False
        for pattern in self.DATE_PATTERNS:
            if re.search(pattern, text):
                return True
        return False

    def _looks_like_amount(self, text: str) -> bool:
        """Check if text looks like a monetary amount."""
        if not text:
            return False
        return bool(re.search(self.AMOUNT_PATTERN, text))

    def _looks_like_transaction_line(self, line: str) -> bool:
        """Check if line looks like a transaction."""
        return self._looks_like_date(line) and self._looks_like_amount(line)

    def _parse_date(self, date_str: str) -> str:
        """Parse date string to YYYY-MM-DD format."""
        if not date_str:
            return None
        try:
            dt = date_parser.parse(date_str, fuzzy=True)
            return dt.strftime('%Y-%m-%d')
        except Exception:
            return None

    def _parse_amount(self, amount_str: str) -> float:
        """Parse amount string to float."""
        if not amount_str:
            return None
        try:
            # Remove currency symbols and commas
            clean = re.sub(r'[$,]', '', amount_str.strip())
            return float(clean)
        except Exception:
            return None

    def _parse_transaction_line(self, line: str) -> Dict[str, Any]:
        """Parse a transaction from a text line."""
        transaction = {}

        # Extract date
        for pattern in self.DATE_PATTERNS:
            match = re.search(pattern, line)
            if match:
                transaction['date'] = self._parse_date(match.group())
                break

        # Extract amounts
        amounts = re.findall(self.AMOUNT_PATTERN, line)
        if amounts:
            transaction['amount'] = self._parse_amount(amounts[0])
            if len(amounts) > 1:
                transaction['balance'] = self._parse_amount(amounts[-1])

        # Extract description (text between date and amount)
        if 'date' in transaction and amounts:
            # Simple heuristic: text after date, before first amount
            parts = re.split(self.AMOUNT_PATTERN, line)
            if len(parts) > 0:
                desc = parts[0]
                # Remove date from description
                for pattern in self.DATE_PATTERNS:
                    desc = re.sub(pattern, '', desc)
                transaction['description'] = desc.strip()

        return transaction if transaction else None

    def to_dataframe(self) -> pd.DataFrame:
        """Convert transactions to pandas DataFrame."""
        if not self.transactions:
            return pd.DataFrame()

        df = pd.DataFrame(self.transactions)

        # Ensure required columns exist
        for col in ['date', 'description', 'amount', 'balance', 'source_file']:
            if col not in df.columns:
                df[col] = None

        # Sort by date
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.sort_values('date')

        # Add category column (placeholder for now)
        df['category'] = 'Uncategorized'

        return df[['date', 'description', 'amount', 'balance', 'category', 'source_file']]


def main():
    parser = argparse.ArgumentParser(description='Extract transactions from PDF bank statements')
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
            pdf_files.append(pattern)  # Keep as-is if not a glob pattern

    # Filter for PDF files
    pdf_files = [f for f in pdf_files if f.lower().endswith('.pdf')]

    if not pdf_files:
        print("ERROR: No PDF files found")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  PDF Transaction Extractor")
    print(f"{'='*60}\n")
    print(f"Found {len(pdf_files)} PDF file(s) to process\n")

    # Extract transactions
    extractor = PDFStatementExtractor()

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
    print(f"Total transactions: {len(df)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Output file: {output_path}")

    if extractor.errors:
        print(f"\nWarnings: {len(extractor.errors)} file(s) had errors")

    print(f"\n✓ Successfully extracted transactions to {output_path}\n")


if __name__ == '__main__':
    main()
