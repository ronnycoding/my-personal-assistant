#!/usr/bin/env python3
"""Add auto-categorization to transactions CSV."""

import csv
from pathlib import Path

def categorize(description):
    """Simple categorization based on keywords."""
    desc_lower = description.lower()

    if any(word in desc_lower for word in ['uber', 'taxi', 'transport']):
        return 'Transportation'
    elif any(word in desc_lower for word in ['restaurant', 'mcdonald', 'burger', 'food', 'bar', 'cafe', 'coffee']):
        return 'Food & Dining'
    elif any(word in desc_lower for word in ['super', 'market', 'mercado', 'ali']):
        return 'Groceries'
    elif any(word in desc_lower for word in ['sinpe', 'tef', 'transfer', 'comision', 'dtr']):
        return 'Transfers'
    elif any(word in desc_lower for word in ['apple', 'amazon', 'netflix', 'spotify', 'prime']):
        return 'Subscriptions'
    elif any(word in desc_lower for word in ['farma', 'pharmacy', 'clinic']):
        return 'Healthcare'
    else:
        return 'Other'

# Read and update CSV
input_file = Path.home() / 'Documents' / 'Finance' / 'transactions-2025.csv'
output_file = Path.home() / 'Documents' / 'Finance' / 'transactions-2025-categorized.csv'

transactions = []
with open(input_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['category'] = categorize(row['description'])
        transactions.append(row)

# Write updated CSV
with open(output_file, 'w', newline='') as f:
    if transactions:
        writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
        writer.writeheader()
        writer.writerows(transactions)

print(f"✓ Categorized {len(transactions)} transactions")
print(f"✓ Saved to: {output_file}")
