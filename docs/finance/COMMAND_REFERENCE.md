# Personal Finance Advisor - Command Reference

Complete reference documentation for all `/finance` commands.

## Table of Contents

- [finance init](#finance-init)
- [finance import](#finance-import)
- [finance analyze](#finance-analyze)
- [finance project](#finance-project)
- [finance advise](#finance-advise)
- [finance report](#finance-report)
- [finance list](#finance-list)
- [finance delete](#finance-delete)

---

## finance init

Create a new financial analysis notebook.

### Syntax
```bash
/finance init --notebook="<name>"
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--notebook` | string | Yes | Notebook name (without .ipynb extension) |

### Examples

```bash
# Create monthly budget notebook
/finance init --notebook="2025-01-budget"

# Create annual planning notebook
/finance init --notebook="2025-financial-plan"

# Create quarterly analysis notebook
/finance init --notebook="2025-Q1-analysis"
```

### Output

Creates a new Jupyter notebook at `.claude/finance-notebooks/<name>.ipynb` with standard template cells.

### Notes

- Notebook names should be filesystem-safe (no special characters except hyphens and underscores)
- Use consistent naming conventions for easy organization
- Notebooks are automatically gitignored for privacy

---

## finance import

Import transaction data from CSV or Excel files.

### Syntax
```bash
/finance import --source="<file_path>" --type="<account_type>" [--notebook="<name>"]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--source` | string | Yes | Path to CSV or Excel file |
| `--type` | string | Yes | Account type: `checking`, `savings`, `credit`, `cash`, `investment` |
| `--notebook` | string | No | Target notebook (uses active if not specified) |

### Supported File Formats

**CSV:**
- Required columns: `date`, `description`, `amount`
- Optional columns: `category`, `account`, `balance`
- Supported date formats: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY
- Encoding: UTF-8 recommended

**Excel:**
- Formats: .xlsx, .xls
- Can specify sheet name or uses first sheet
- Same column requirements as CSV

### Example CSV Format

```csv
date,description,amount
2025-01-15,Grocery Store,-125.50
2025-01-16,Direct Deposit,3500.00
2025-01-17,Electric Company,-89.23
```

### Examples

```bash
# Import checking account transactions
/finance import --source="./checking-jan2025.csv" --type="checking"

# Import credit card statement
/finance import --source="./creditcard-statement.xlsx" --type="credit"

# Import to specific notebook
/finance import --source="./transactions.csv" --type="checking" --notebook="2025-budget"
```

### Data Processing

The import process automatically:

1. **Validates data** - Checks required columns and data types
2. **Parses dates** - Handles multiple date formats
3. **Categorizes transactions** - Uses keyword matching (see [Categories](#transaction-categories))
4. **Detects duplicates** - Exact and fuzzy matching
5. **Cleans data** - Removes invalid entries, future dates, zero amounts
6. **Stores in notebook** - Appends to existing data or creates new

### Transaction Categories

Auto-categorization uses these categories:

- **income**: salary, paycheck, deposit, bonus, refund
- **housing**: rent, mortgage, utilities, insurance
- **food_dining**: restaurant, grocery, cafe, delivery
- **transportation**: uber, gas, parking, transit
- **shopping**: amazon, target, walmart, online
- **healthcare**: pharmacy, doctor, medical, dental
- **entertainment**: netflix, spotify, movie, subscription
- **travel**: hotel, flight, airline, vacation
- **education**: tuition, school, course, books
- **personal**: haircut, gym, salon, fitness
- **bills**: phone, internet, cable, utilities
- **transfer**: transfer, withdrawal, atm
- **fees**: fee, charge, penalty
- **uncategorized**: didn't match any keywords

### Output Example

```
✓ Imported 247 transactions from checking-jan2025.csv
✓ Date range: 2024-01-01 to 2025-01-31
✓ Duplicates skipped: 3
✓ Auto-categorized: 234/247 (95%)
✓ Uncategorized: 13 transactions

Category Summary:
- Income: 28 transactions, $21,000.00
- Housing: 12 transactions, $6,300.00
- Food & Dining: 45 transactions, $1,245.80
- Transportation: 18 transactions, $890.50
...

Stored in notebook: 2025-budget
Cell: "Transaction Data" (row 4)
```

---

## finance analyze

Analyze financial data and calculate metrics.

### Syntax
```bash
/finance analyze --type="<analysis_type>" [--period="<time_range>"] [--notebook="<name>"]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--type` | string | Yes | Analysis type (see [Analysis Types](#analysis-types)) |
| `--period` | string | No | Time range (default: "last-12-months") |
| `--notebook` | string | No | Target notebook (uses active if not specified) |

### Analysis Types

| Type | Description | Output |
|------|-------------|--------|
| `overview` | Comprehensive financial summary | Income, expenses, cash flow, savings rate, health score |
| `income` | Income analysis and sources | Total income, sources breakdown, trends |
| `expenses` | Expense analysis by category | Total expenses, category breakdown, top expenses |
| `cashflow` | Net cash flow trends | Monthly/quarterly cash flow, burn rate |
| `networth` | Assets, liabilities, net worth | Account balances, net worth calculation, trend |
| `savings` | Savings metrics | Savings rate, emergency fund ratio, progress |
| `budget` | Budget vs. actual comparison | Variance by category, over/under budget |

### Time Period Options

- `last-month` - Previous 30 days
- `last-3-months` - Previous 90 days
- `last-6-months` - Previous 180 days
- `last-12-months` - Previous 365 days (default)
- `this-month` - Current month to date
- `this-quarter` - Current quarter to date
- `this-year` - Current year to date
- `ytd` - Year to date (same as this-year)
- `2024` - Specific year
- `2024-Q1` - Specific quarter
- `all` - All available data

### Examples

```bash
# Comprehensive overview
/finance analyze --type=overview

# Last 3 months overview
/finance analyze --type=overview --period="last-3-months"

# Expense breakdown this month
/finance analyze --type=expenses --period="this-month"

# Annual income analysis
/finance analyze --type=income --period="2024"

# Budget comparison
/finance analyze --type=budget --period="this-month"
```

### Output - Overview Example

```
Financial Overview (Last 12 Months)
====================================

💰 Income
Total Income:                    $84,000.00
Average Monthly Income:          $7,000.00
Income Sources:
  - Salary (Direct Deposit):     $84,000.00 (100%)

💸 Expenses
Total Expenses:                  $64,938.00
Average Monthly Expenses:        $5,411.50
Burn Rate:                       $5,411.50/month

Category Breakdown:
  1. Housing:                    $25,200.00 (39%)
  2. Food & Dining:              $14,694.00 (23%)
  3. Transportation:             $8,460.00 (13%)
  4. Shopping:                   $7,553.00 (12%)
  5. Utilities:                  $5,057.00 (8%)
  6. Entertainment:              $2,599.00 (4%)
  7. Healthcare:                 $1,300.00 (2%)

📊 Cash Flow
Net Cash Flow:                   $19,062.00
Monthly Average:                 $1,588.50
Trend:                           Positive ↗

💵 Savings
Savings Rate:                    22.7%
Emergency Fund:                  $17,500 (3.2 months)
Recommended:                     6 months ($32,466)

❤️  Financial Health Score:      78/100 (Good)

Breakdown:
  - Savings Rate (30pts):        25/30 (Good - above 20%)
  - Emergency Fund (25pts):      13/25 (Fair - need 6 months)
  - Debt-to-Income (20pts):      20/20 (Excellent - minimal debt)
  - Budget Adherence (15pts):    12/15 (Good - minor variances)
  - Cash Flow Trend (10pts):     8/10 (Positive trend)

✓ Strengths:
  - Strong savings rate (above 20% target)
  - Positive cash flow every month
  - Minimal debt burden
  - Consistent income

⚠ Areas to Improve:
  - Emergency fund below 6-month target
  - Discretionary spending at 35% (target: <30%)
  - No investment contributions detected
```

---

## finance project

Generate financial projections and forecasts.

### Syntax
```bash
/finance project --type="<projection_type>" [--months=<number>] [--scenario="<name>"] [--notebook="<name>"]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--type` | string | Yes | Projection type (see [Projection Types](#projection-types)) |
| `--months` | number | No | Number of months to project (default: 12) |
| `--scenario` | string | No | Scenario: `conservative`, `moderate`, `aggressive` (default: moderate) |
| `--notebook` | string | No | Target notebook |

### Projection Types

| Type | Description |
|------|-------------|
| `cashflow` | Monthly income/expense projections |
| `savings` | Savings goal progress and timeline |
| `networth` | Net worth projection over time |
| `debt` | Debt payoff schedule |
| `retirement` | Retirement savings projection |

### Scenario Parameters

| Scenario | Income Growth | Expense Growth | Investment Return |
|----------|---------------|----------------|-------------------|
| Conservative | 2% annual | 3% annual | 5% annual |
| Moderate | 4% annual | 3% annual | 7% annual |
| Aggressive | 6% annual | 2% annual | 10% annual |

### Examples

```bash
# 12-month cash flow projection (moderate scenario)
/finance project --type=cashflow --months=12

# Conservative 24-month projection
/finance project --type=cashflow --months=24 --scenario="conservative"

# Savings goal progress
/finance project --type=savings --goal-amount=50000 --months=24

# Retirement planning (30-year projection)
/finance project --type=retirement --months=360

# Debt payoff schedule
/finance project --type=debt --principal=25000 --interest-rate=0.05 --monthly-payment=500
```

### Output - Cash Flow Projection Example

```
12-Month Cash Flow Projection
==============================

Scenario: Moderate
Assumptions:
  - Base monthly income: $7,000
  - Income growth: 4% annually (0.33% monthly)
  - Base monthly expenses: $5,412
  - Expense growth: 3% annually (0.25% monthly)

Month    Income       Expenses     Cash Flow    Cumulative
------------------------------------------------------------
Jan 25   $7,023.10    $5,425.53    $1,597.57    $1,597.57
Feb 25   $7,046.33    $5,439.09    $1,607.24    $3,204.81
Mar 25   $7,069.69    $5,452.68    $1,617.01    $4,821.82
Apr 25   $7,093.17    $5,466.31    $1,626.86    $6,448.68
May 25   $7,116.78    $5,479.97    $1,636.81    $8,085.49
Jun 25   $7,140.51    $5,493.67    $1,646.84    $9,732.33
Jul 25   $7,164.37    $5,507.40    $1,656.97    $11,389.30
Aug 25   $7,188.36    $5,521.16    $1,667.20    $13,056.50
Sep 25   $7,212.47    $5,534.96    $1,677.51    $14,734.01
Oct 25   $7,236.71    $5,548.79    $1,687.92    $16,421.93
Nov 25   $7,261.07    $5,562.66    $1,698.41    $18,120.34
Dec 25   $7,285.56    $5,576.56    $1,709.00    $19,829.34

Summary:
  - Projected annual income: $86,838.12 (+3.4%)
  - Projected annual expenses: $66,008.78 (+1.7%)
  - Projected annual savings: $20,829.34
  - Average monthly surplus: $1,735.78
  - Savings rate: 24.0%

✓ On track to exceed 20% savings rate target
✓ Positive cash flow every month
✓ Growing monthly surplus over time
```

---

## finance advise

Get AI-driven financial recommendations.

### Syntax
```bash
/finance advise [--focus="<area>"] [--goal="<objective>"] [--notebook="<name>"]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--focus` | string | No | Focus area (see [Focus Areas](#focus-areas)) |
| `--goal` | string | No | Specific financial goal |
| `--notebook` | string | No | Target notebook |

### Focus Areas

| Focus | Description |
|-------|-------------|
| `overall` | Comprehensive financial advice (default) |
| `budget` | Budget optimization suggestions |
| `savings` | Savings acceleration strategies |
| `debt` | Debt reduction guidance |
| `spending` | Spending pattern improvements |
| `goals` | Financial goal planning |

### Examples

```bash
# Comprehensive advice
/finance advise

# Budget optimization
/finance advise --focus="budget"

# Savings strategies
/finance advise --focus="savings"

# With specific goal
/finance advise --focus="savings" --goal="Save $50k for house down payment"
```

### Output Example

```
AI Financial Recommendations
=============================

Focus: Savings Acceleration
Goal: Build emergency fund to 6 months

Current Financial Situation:
  - Monthly income: $7,000
  - Monthly expenses: $5,412
  - Savings rate: 22.7%
  - Emergency fund: $17,500 (3.2 months)
  - Target: $32,472 (6 months of expenses)
  - Gap: $14,972

═══════════════════════════════════════════════════

Top 3 Priority Recommendations:

[1] 🔴 HIGH PRIORITY - Build Emergency Fund to 6 Months

Current: $17,500 (3.2 months)
Target: $32,472 (6 months)
Shortfall: $14,972

Timeline & Strategy:
  - Allocate $1,247/month for 12 months
  - Source: Redirect $800 current surplus + $447 from optimizations below
  - Expected completion: January 2026

Action Items:
  ☐ Set up automated monthly transfer: $1,247 to savings
  ☐ Choose high-yield savings account (5%+ APY)
  ☐ Review progress monthly

Impact: Financial security for 6+ months of unemployment/emergency

─────────────────────────────────────────────────

[2] 🟡 MEDIUM PRIORITY - Optimize Food & Dining Budget

Current Spending: $1,224.50/month (22.6% of expenses)
Benchmark: Should be 10-15% ($541-$812)
Potential Savings: $412-$684/month

Specific Actions:
  ☐ Meal prep on Sundays (Save ~$120/month)
    - Reduces weekday lunches from $15 → $5
    - Cook dinner 5 nights/week instead of 3

  ☐ Limit dining out to 2x per week (Save ~$180/month)
    - Current: ~6 times/week at $30/meal
    - Target: 2 times/week

  ☐ Use grocery cashback apps (Save ~$50/month)
    - Ibotta, Fetch, Checkout 51
    - 3-5% cash back on groceries

  ☐ Shop with list to avoid impulse purchases (Save ~$80/month)

Total Monthly Savings: $430
Annual Impact: $5,160

─────────────────────────────────────────────────

[3] 🟡 MEDIUM PRIORITY - Review and Optimize Subscriptions

Current Subscriptions: 8 services
Monthly Cost: $157
Underutilized Services Identified:

  • Premium Gym - $89/month
    Usage: 1.2 visits/week (low)
    Action: Switch to basic gym ($30) or home workouts
    Savings: $59/month

  • Streaming Bundle - $35/month
    Services: Netflix, Hulu, Disney+
    Usage: Primarily Netflix
    Action: Rotate services quarterly
    Savings: $23/month (average)

  • Audiobook subscription - $15/month
    Usage: 0.5 books/month
    Action: Use library app (Libby) instead
    Savings: $15/month

Total Monthly Savings: $97
Annual Impact: $1,164

─────────────────────────────────────────────────

💡 Additional Quick Wins:

4. Increase 401(k) contribution to get full employer match
   Current: 3% ($210/month)
   Employer match: Up to 5%
   Recommended: 5% ($350/month)
   Impact: $140/month free money + tax savings

5. Set up savings account with better interest rate
   Current: 0.5% APY at MegaBank
   High-yield options: 5.0%+ APY
   On $17,500: +$787/year passive income

─────────────────────────────────────────────────

📊 Combined Impact Summary:

Monthly Savings Potential: $527
  - Food & Dining optimization: $430
  - Subscription cuts: $97

Applied to Emergency Fund Goal:
  - Current plan: 12 months to goal
  - With optimizations: 9.5 months to goal
  - Accelerated by: 2.5 months

Next Steps:
1. Implement top priority action items this week
2. Track progress for one month
3. Re-run analysis: /finance analyze --type=overview
4. Reassess recommendations: /finance advise --focus="savings"

═══════════════════════════════════════════════════

⚠️  Disclaimer: This AI-generated advice is for informational purposes
only and does not constitute professional financial advice. Consider
consulting a certified financial planner for personalized guidance.
```

---

## finance report

Create visualizations and reports.

### Syntax
```bash
/finance report --type="<chart_type>" [--period="<time_range>"] [--format="<output>"] [--notebook="<name>"]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--type` | string | Yes | Chart type (see [Chart Types](#chart-types)) |
| `--period` | string | No | Time range (default: "last-12-months") |
| `--format` | string | No | Output: `inline`, `png`, `pdf` (default: inline) |
| `--notebook` | string | No | Target notebook |

### Chart Types

| Type | Visualization | Purpose |
|------|---------------|---------|
| `income-expense` | Line/bar chart | Income vs expenses over time |
| `categories` | Pie chart | Spending breakdown by category |
| `networth` | Area chart | Net worth trend over time |
| `cashflow` | Waterfall chart | Income sources and expense categories |
| `budget` | Grouped bar chart | Budget vs actual comparison |
| `projections` | Line chart with bands | Future projections with confidence intervals |

### Examples

```bash
# Income vs expenses trend
/finance report --type="income-expense" --period="last-12-months"

# Export to PNG
/finance report --type="categories" --format="png"

# Budget comparison
/finance report --type="budget" --period="this-month"

# Net worth tracking
/finance report --type="networth" --period="all"
```

### Output

Charts are displayed inline in the notebook. When exported, files are saved to `.claude/finance-notebooks/reports/`.

---

## finance list

List all financial notebooks.

### Syntax
```bash
/finance list
```

### Output Example

```
Financial Notebooks
===================

Active: 2025-budget ✓

Available Notebooks:
  1. 2025-budget.ipynb
     Created: 2025-01-01
     Modified: 2025-01-28 10:45 AM
     Size: 245 KB
     Status: Active

  2. 2024-annual-review.ipynb
     Created: 2024-01-01
     Modified: 2024-12-31 05:30 PM
     Size: 512 KB
     Status: Archived

  3. 2025-Q1-planning.ipynb
     Created: 2025-01-15
     Modified: 2025-01-20 02:15 PM
     Size: 128 KB
     Status: Inactive

Total: 3 notebooks
```

---

## finance delete

Delete a financial notebook.

### Syntax
```bash
/finance delete --notebook="<name>" [--confirm]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--notebook` | string | Yes | Notebook name to delete |
| `--confirm` | flag | No | Skip confirmation prompt |

### Examples

```bash
# Delete with confirmation
/finance delete --notebook="old-budget"

# Delete without confirmation
/finance delete --notebook="old-budget" --confirm
```

### Output

```
⚠️  WARNING: This will permanently delete the notebook and all its data!

Notebook: old-budget.ipynb
Created: 2024-01-01
Last modified: 2024-12-31
Transactions: 1,247
Size: 512 KB

This action cannot be undone.

Confirm deletion? (yes/no): yes

✓ Notebook deleted: old-budget.ipynb
✓ Backup created: .claude/finance-notebooks/.backups/old-budget-2025-01-28.ipynb
```

---

## Common Patterns

### Monthly Finance Routine

```bash
# 1. Import transactions
/finance import --source="checking.csv" --type="checking"
/finance import --source="credit.csv" --type="credit"

# 2. Analyze the month
/finance analyze --type=overview --period="this-month"

# 3. Check budget adherence
/finance analyze --type=budget --period="this-month"

# 4. Create reports
/finance report --type="categories" --period="this-month"

# 5. Get recommendations
/finance advise --focus="budget"
```

### Annual Planning

```bash
# 1. Create new year notebook
/finance init --notebook="2025-plan"

# 2. Import last year's data
/finance import --source="2024-all-transactions.csv"

# 3. Analyze trends
/finance analyze --type=overview --period="2024"

# 4. Project next year
/finance project --type=cashflow --months=12 --scenario="moderate"

# 5. Set goals and get advice
/finance advise --focus="goals" --goal="Save $50k for house"
```

### Financial Health Check

```bash
# 1. Comprehensive analysis
/finance analyze --type=overview --period="last-12-months"

# 2. Check savings progress
/finance analyze --type=savings

# 3. Review net worth
/finance analyze --type=networth

# 4. Get overall recommendations
/finance advise --focus="overall"

# 5. Create visual dashboard
/finance report --type="income-expense" --period="last-12-months"
/finance report --type="networth" --period="all"
```

---

## See Also

- [Quick Start Guide](QUICK_START.md)
- [Tutorials](TUTORIALS.md)
- [API Reference](API_REFERENCE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Privacy & Security](PRIVACY_SECURITY.md)
