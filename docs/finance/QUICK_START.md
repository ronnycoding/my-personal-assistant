# Personal Finance Advisor - Quick Start Guide

Get started with the `/finance` command in under 10 minutes!

## Prerequisites

- Claude Code installed and configured
- jupyter-mcp server running (check with `claude mcp list`)
- Python 3.8+ with pandas, numpy, matplotlib installed

## Step 1: Create Your First Financial Notebook

```bash
/finance init --notebook="2025-budget"
```

This creates a new Jupyter notebook at `.claude/finance-notebooks/2025-budget.ipynb` with:
- Pre-configured setup cells
- Standard financial data schemas
- Placeholder cells for analysis, projections, and recommendations

**Expected Output:**
```
✓ Created financial notebook: 2025-budget
✓ Notebook path: .claude/finance-notebooks/2025-budget.ipynb
✓ Kernel: python3 (active)

Next steps:
1. Import your transaction data: /finance import --source="transactions.csv"
2. Update account balances in the notebook
3. Run analysis: /finance analyze --type=overview
```

## Step 2: Import Your Transactions

First, export your bank transactions to CSV format. Most banks allow downloading:
- Checking account transactions
- Savings account transactions
- Credit card statements

**CSV Format Example:**
```csv
date,description,amount
2025-01-15,Grocery Store,-125.50
2025-01-16,Paycheck,3500.00
2025-01-17,Electric Bill,-89.23
```

Then import:

```bash
/finance import --source="./checking-transactions.csv" --type="checking"
```

**What happens:**
1. ✓ Validates CSV format and data
2. ✓ Parses dates (supports multiple formats)
3. ✓ Automatically categorizes transactions (food, housing, income, etc.)
4. ✓ Detects and skips duplicates
5. ✓ Stores in your notebook's "Transaction Data" cell

**Expected Output:**
```
✓ Imported 247 transactions from checking-transactions.csv
✓ Date range: 2024-01-01 to 2025-01-31
✓ Duplicates skipped: 0
✓ Auto-categorized: 234/247 (95%)
✓ Uncategorized: 13 (review needed)

Top categories:
- Income: $7,000.00 (28 transactions)
- Housing: $2,100.00 (12 transactions)
- Food & Dining: $1,245.80 (45 transactions)
```

## Step 3: Analyze Your Finances

Run a comprehensive financial overview:

```bash
/finance analyze --type=overview --period="last-3-months"
```

**Expected Output:**
```
Financial Overview (Last 3 Months)
=====================================

Income:                  $21,000.00
Expenses:                $16,234.50
Net Cash Flow:           $4,765.50
Savings Rate:            22.7%

Top Expense Categories:
1. Housing               $6,300.00 (39%)
2. Food & Dining         $3,680.45 (23%)
3. Transportation        $2,100.00 (13%)
4. Shopping              $1,890.30 (12%)
5. Utilities             $1,264.25 (8%)

Financial Health Score: 78/100 (Good)

Strengths:
✓ Strong savings rate (>20%)
✓ Positive cash flow trend
✓ Expenses under control

Areas to improve:
⚠ Emergency fund: 3.2 months (target: 6 months)
⚠ Discretionary spending: 35% of income (target: <30%)
```

## Step 4: Generate Projections

See where your finances are heading:

```bash
/finance project --type=cashflow --months=12 --scenario="moderate"
```

**Expected Output:**
```
12-Month Cash Flow Projection (Moderate Scenario)
=================================================

Assumptions:
- Income growth: 4% annually
- Expense growth: 3% annually
- Current monthly income: $7,000
- Current monthly expenses: $5,411

Month    Income      Expenses    Cash Flow    Cumulative
------------------------------------------------------------
Jan 25   $7,023      $5,425      $1,598       $1,598
Feb 25   $7,047      $5,438      $1,609       $3,207
Mar 25   $7,070      $5,451      $1,619       $4,826
Apr 25   $7,093      $5,465      $1,628       $6,454
...
Dec 25   $7,280      $5,575      $1,705       $19,750

Projected annual savings: $19,750
On track to meet 2025 savings goal: ✓
```

## Step 5: Get AI Recommendations

Receive personalized financial advice:

```bash
/finance advise --focus="savings"
```

**Expected Output:**
```
AI Financial Recommendations - Savings Acceleration
===================================================

Current Situation:
- Savings rate: 22.7% (Excellent)
- Emergency fund: 3.2 months (Needs improvement)
- Monthly surplus: $1,588 average

Top 3 Recommendations:

1. [HIGH PRIORITY] Build Emergency Fund
   Current: $17,500 (3.2 months)
   Target: $32,000 (6 months)
   Gap: $14,500

   Action: Allocate $1,200/month for 12 months
   - Reduce discretionary spending by $400/month
   - Redirect existing $800 monthly surplus
   Expected completion: February 2026

2. [MEDIUM PRIORITY] Optimize Food & Dining Budget
   Current spending: $1,227/month
   Potential savings: $250/month (20% reduction)

   Specific actions:
   - Meal prep Sundays: Save $120/month
   - Reduce dining out to 2x/week: Save $80/month
   - Use grocery cashback apps: Save $50/month

3. [MEDIUM PRIORITY] Review Subscriptions
   Identified subscriptions: 7 services, $143/month
   Underutilized: Netflix, Spotify Premium, Gym ($67/month)

   Action: Cancel or downgrade unused services
   Potential savings: $67/month = $804/year

Total monthly savings potential: $517
Annual impact: $6,204
```

## Step 6: Create Visual Reports

Generate charts and graphs:

```bash
/finance report --type="income-expense" --period="last-12-months"
```

This creates an interactive chart showing your income vs. expenses over time, with trend lines and cash flow visualization.

Other report types:
```bash
# Category spending breakdown (pie chart)
/finance report --type="categories" --period="last-3-months"

# Net worth tracking over time
/finance report --type="networth" --period="all"

# Budget vs. actual comparison
/finance report --type="budget" --period="this-month"
```

## Common Workflows

### Monthly Review Workflow
```bash
# 1. Import this month's transactions
/finance import --source="checking-jan2025.csv" --type="checking"

# 2. Update account balances in notebook

# 3. Run monthly analysis
/finance analyze --type=overview --period="this-month"

# 4. Create spending report
/finance report --type="categories" --period="this-month"

# 5. Compare to budget
/finance analyze --type=budget --period="this-month"

# 6. Get recommendations
/finance advise --focus="budget"
```

### Financial Planning Workflow
```bash
# 1. Set up yearly notebook
/finance init --notebook="2025-financial-plan"

# 2. Import historical data
/finance import --source="2024-all-transactions.csv"

# 3. Analyze trends
/finance analyze --type=overview --period="all"

# 4. Create 12-month projection
/finance project --type=cashflow --months=12 --scenario="moderate"

# 5. Set savings goals
/finance project --type=savings --goal-amount=50000

# 6. Get comprehensive advice
/finance advise --focus="overall"
```

## Tips for Success

1. **Import transactions regularly** (weekly or monthly) to keep data fresh
2. **Update account balances** in your notebook whenever they change significantly
3. **Review categories** - the auto-categorization is 90%+ accurate but check uncategorized items
4. **Use consistent notebook naming** - e.g., `2025-budget`, `2025-Q1`, `2025-annual`
5. **Archive old notebooks** - keep 1-2 years of history, archive older
6. **Backup notebooks** - they contain sensitive data and are gitignored
7. **Re-run analyses** after importing new data to see updated metrics

## Troubleshooting

**"MCP server not found"**
- Check jupyter-mcp is running: `claude mcp list`
- Verify MCP configuration in Claude Code settings

**"Import failed: Invalid date format"**
- Check your CSV uses standard date formats (YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY)
- Ensure date column is named 'date' or specify column mapping

**"Notebook not found"**
- Use `/finance list` to see all available notebooks
- Check notebook name spelling (case-sensitive)

**"No transactions found"**
- Verify CSV file path is correct
- Check CSV has 'date', 'description', 'amount' columns
- Ensure amounts are numeric (no currency symbols in file)

## Next Steps

- Read the [Command Reference](COMMAND_REFERENCE.md) for detailed command documentation
- Explore [Tutorials](TUTORIALS.md) for step-by-step guides
- Check [Privacy & Security](PRIVACY_SECURITY.md) for data protection best practices

## Getting Help

- Review [Troubleshooting Guide](TROUBLESHOOTING.md)
- Check the [API Reference](API_REFERENCE.md) for developers
- File issues at: https://github.com/ronnycoding/my-personal-agents/issues
