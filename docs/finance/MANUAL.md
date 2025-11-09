# Personal Finance Advisor - Complete Manual

Comprehensive reference manual for all `/finance` command options and parameters.

## Table of Contents

- [Command Overview](#command-overview)
- [finance init](#finance-init)
- [finance import](#finance-import)
- [finance analyze](#finance-analyze)
- [finance project](#finance-project)
- [finance advise](#finance-advise)
- [finance report](#finance-report)
- [finance list](#finance-list)
- [finance delete](#finance-delete)

---

## Command Overview

| Command | Primary Function | Parameters | Dependencies |
|---------|------------------|------------|--------------|
| `init` | Create notebook | 1 required | jupyter-mcp |
| `import` | Import data | 2 required, 1 optional | Active notebook |
| `analyze` | Analyze finances | 1 required, 2 optional | Transaction data |
| `project` | Generate forecasts | 1 required, 3 optional | Transaction data |
| `advise` | AI recommendations | 3 optional | Analysis data |
| `report` | Create visualizations | 1 required, 3 optional | Transaction data |
| `list` | List notebooks | None | jupyter-mcp |
| `delete` | Remove notebook | 1 required, 1 optional | None |

---

## finance init

**Purpose**: Create a new financial analysis notebook with template structure.

### Syntax

```bash
/finance init --notebook="<notebook_name>"
```

### Parameters

| Parameter | Type | Required | Default | Description | Valid Values |
|-----------|------|----------|---------|-------------|--------------|
| `--notebook` | string | Yes | None | Notebook name (without .ipynb) | Alphanumeric, hyphens, underscores |

### Behavior

1. Creates new Jupyter notebook at `.claude/finance-notebooks/<name>.ipynb`
2. Initializes Python kernel
3. Inserts 14 template cells from `FINANCE_NOTEBOOK_TEMPLATE.md`
4. Sets notebook as active for subsequent commands
5. Creates notebook metadata (creation date, currency, version)

### Examples

```bash
# Monthly budget notebook
/finance init --notebook="2025-01-budget"

# Annual planning notebook
/finance init --notebook="2025-financial-plan"

# Quarterly review
/finance init --notebook="2025-Q1-review"

# Goal-specific notebook
/finance init --notebook="house-downpayment-goal"
```

### Output

```
✓ Created financial notebook: 2025-01-budget
✓ Notebook path: .claude/finance-notebooks/2025-01-budget.ipynb
✓ Kernel: python3 (active)
✓ Template cells: 14 inserted

Next steps:
1. Import transactions: /finance import --source="transactions.csv" --type="checking"
2. Update account balances in notebook
3. Run analysis: /finance analyze --type=overview
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "Notebook already exists" | File with same name exists | Use different name or delete existing |
| "Invalid notebook name" | Special characters in name | Use only letters, numbers, hyphens, underscores |
| "jupyter-mcp not available" | MCP server not running | Start jupyter-mcp server |

---

## finance import

**Purpose**: Import transaction data from CSV or Excel files into active notebook.

### Syntax

```bash
/finance import --source="<file_path>" --type="<account_type>" [--notebook="<name>"]
```

### Parameters

| Parameter | Type | Required | Default | Description | Valid Values |
|-----------|------|----------|---------|-------------|--------------|
| `--source` | string | Yes | None | Path to CSV/Excel file | Valid file path |
| `--type` | string | Yes | None | Account type | `checking`, `savings`, `credit`, `cash`, `investment` |
| `--notebook` | string | No | Active | Target notebook name | Any existing notebook |

### Account Types

| Type | Description | Amount Convention | Use Case |
|------|-------------|-------------------|----------|
| `checking` | Checking accounts | Positive=deposit, Negative=withdrawal | Daily transactions |
| `savings` | Savings accounts | Positive=deposit, Negative=withdrawal | Savings tracking |
| `credit` | Credit cards | Positive=payment, Negative=purchase | Credit card bills |
| `cash` | Cash transactions | Positive=received, Negative=spent | Cash flow |
| `investment` | Investment accounts | Positive=contribution, Negative=withdrawal | Portfolio tracking |

### File Format Requirements

**CSV Format:**
```csv
date,description,amount
2025-01-15,Grocery Store,-125.50
2025-01-16,Direct Deposit,3500.00
```

**Required Columns:**
- `date` (or Date, Transaction Date, Posting Date)
- `description` (or Description, Details, Merchant, Payee)
- `amount` (or Amount, Debit, Credit, Transaction Amount)

**Optional Columns:**
- `category` - Pre-assigned category
- `account` - Account identifier
- `balance` - Running balance
- `type` - Transaction type (debit/credit)

**Supported Date Formats:**
- `YYYY-MM-DD` (2025-01-15)
- `MM/DD/YYYY` (01/15/2025)
- `DD/MM/YYYY` (15/01/2025)
- `YYYY-MM-DD HH:MM:SS` (2025-01-15 14:30:00)
- `Jan 15, 2025`
- `January 15, 2025`

### Data Processing Pipeline

| Step | Action | Details |
|------|--------|---------|
| 1. Load | Read file | CSV/Excel detection |
| 2. Validate | Check schema | Required columns, data types |
| 3. Parse | Date parsing | Multiple format support |
| 4. Categorize | Auto-categorize | 14 categories, keyword matching |
| 5. Deduplicate | Remove duplicates | Exact and fuzzy matching |
| 6. Clean | Remove invalid | Future dates, zero amounts, nulls |
| 7. Merge | Combine with existing | Append to notebook data |
| 8. Store | Save to notebook | Update "Transaction Data" cell |

### Transaction Categories

| Category | Keywords | Example Transactions |
|----------|----------|---------------------|
| `income` | salary, paycheck, deposit, bonus | Direct Deposit, Paycheck |
| `housing` | rent, mortgage, utilities, insurance | Rent Payment, Electric Bill |
| `food_dining` | restaurant, grocery, cafe, delivery | Whole Foods, Starbucks |
| `transportation` | uber, gas, parking, transit | Gas Station, Uber |
| `shopping` | amazon, target, walmart | Amazon.com, Target |
| `healthcare` | pharmacy, doctor, medical | CVS Pharmacy, Doctor Visit |
| `entertainment` | netflix, spotify, movie | Netflix, Movie Theater |
| `travel` | hotel, flight, airline | Southwest Airlines, Hilton |
| `education` | tuition, school, course | University Tuition |
| `personal` | haircut, gym, salon | LA Fitness, Haircut |
| `bills` | phone, internet, cable | Verizon, Comcast |
| `transfer` | transfer, withdrawal, atm | ATM Withdrawal |
| `fees` | fee, charge, penalty | Overdraft Fee |
| `uncategorized` | No match found | Unknown transactions |

### Examples

#### Direct Import (CSV/Excel)

```bash
# Import checking account from CSV
/finance import --source="~/Documents/Finance/checking.csv" --type="checking"

# Import credit card statement from Excel
/finance import --source="~/Downloads/amex-jan.xlsx" --type="credit"

# Import to specific notebook
/finance import --source="./savings.csv" --type="savings" --notebook="2025-budget"

# Import with full path
/finance import --source="/Users/username/Documents/statements/transactions.csv" --type="checking"
```

#### Import from PDF Statements

**Step 1: Extract transactions from PDF**

```bash
# Navigate to finance tools directory
cd .claude/finance-notebooks

# Extract from single PDF
python extract_pdf_statements.py \
  ~/Documents/Finance/statement-jan.pdf \
  -o ~/Documents/Finance/jan-transactions.csv

# Extract from multiple PDFs
python extract_pdf_statements.py \
  ~/Documents/Finance/statements/*.pdf \
  -o ~/Documents/Finance/all-2024.csv
```

**Step 2: Import the extracted CSV**

```bash
# Import extracted transactions
/finance import --source="~/Documents/Finance/jan-transactions.csv" --type="checking"

# Or import combined file from multiple PDFs
/finance import --source="~/Documents/Finance/all-2024.csv" --type="checking"
```

#### Import Multiple Files (Consolidation)

**Step 1: Consolidate multiple CSV/Excel files**

```bash
# Navigate to finance tools directory
cd .claude/finance-notebooks

# Combine multiple checking account files
python consolidate_statements.py \
  ~/Documents/Finance/checking-jan.csv \
  ~/Documents/Finance/checking-feb.csv \
  ~/Documents/Finance/checking-mar.csv \
  -o ~/Documents/Finance/q1-checking.csv

# Or use wildcards
python consolidate_statements.py \
  ~/Documents/Finance/checking-*.csv \
  -o ~/Documents/Finance/2024-checking-all.csv
```

**Step 2: Import the consolidated file**

```bash
/finance import --source="~/Documents/Finance/q1-checking.csv" --type="checking"
```

#### Complete Workflow: PDF to Analysis

```bash
# 1. Extract all PDFs for the year
cd .claude/finance-notebooks
python extract_pdf_statements.py \
  ~/Documents/Finance/2024/*.pdf \
  -o ~/Documents/Finance/2024-all.csv

# 2. Create annual notebook
/finance init --notebook="2024-annual"

# 3. Import extracted data
/finance import --source="~/Documents/Finance/2024-all.csv" --type="checking"

# 4. Analyze immediately
/finance analyze --type=overview --period="2024"

# 5. Clean up source files (data now in gitignored notebook)
rm ~/Documents/Finance/2024-all.csv
```

### Output

```
✓ Imported 247 transactions from checking.csv
✓ Date range: 2024-01-01 to 2025-01-31
✓ Duplicates skipped: 3
✓ Auto-categorized: 234/247 (95%)
✓ Uncategorized: 13 transactions (review needed)

Category Summary:
  Income:           28 transactions,  $21,000.00
  Housing:          12 transactions,   $6,300.00
  Food & Dining:    45 transactions,   $1,245.80
  Transportation:   18 transactions,     $890.50
  Shopping:         32 transactions,   $1,456.30
  Bills:             8 transactions,     $567.00
  Entertainment:    15 transactions,     $345.00
  Uncategorized:    13 transactions,     $234.50

Stored in notebook: 2025-budget (Cell 4: Transaction Data)
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "File not found" | Invalid path | Check file path, use absolute path |
| "Invalid file format" | Not CSV/Excel | Convert to CSV or Excel |
| "Missing required columns" | Schema mismatch | Ensure date, description, amount columns |
| "No valid transactions" | All rows invalid | Check date and amount formats |
| "No active notebook" | No notebook selected | Run `/finance init` or specify `--notebook` |

---

## finance analyze

**Purpose**: Analyze financial data and calculate key metrics.

### Syntax

```bash
/finance analyze --type="<analysis_type>" [--period="<time_range>"] [--notebook="<name>"]
```

### Parameters

| Parameter | Type | Required | Default | Description | Valid Values |
|-----------|------|----------|---------|-------------|--------------|
| `--type` | string | Yes | None | Type of analysis | See Analysis Types table |
| `--period` | string | No | `last-12-months` | Time range to analyze | See Time Period Options table |
| `--notebook` | string | No | Active | Target notebook | Any existing notebook |

### Analysis Types

| Type | Description | Metrics Calculated | Output |
|------|-------------|-------------------|--------|
| `overview` | Comprehensive summary | Income, expenses, cash flow, savings rate, health score | Full financial dashboard |
| `income` | Income analysis | Total income, monthly average, sources breakdown, trends | Income report |
| `expenses` | Expense analysis | Total expenses, category breakdown, top 10 expenses | Expense report |
| `cashflow` | Cash flow trends | Monthly net flow, burn rate, trend direction | Cash flow analysis |
| `networth` | Net worth calculation | Assets, liabilities, net worth, trend | Net worth statement |
| `savings` | Savings metrics | Savings rate, emergency fund ratio, goals progress | Savings analysis |
| `budget` | Budget comparison | Actual vs budget by category, variance, overspend | Budget variance report |

### Time Period Options

| Period | Description | Date Range | Example Use |
|--------|-------------|------------|-------------|
| `last-month` | Previous 30 days | Today - 30 days | Recent activity |
| `last-3-months` | Previous 90 days | Today - 90 days | Quarterly review |
| `last-6-months` | Previous 180 days | Today - 180 days | Semi-annual |
| `last-12-months` | Previous 365 days | Today - 365 days | Annual review (default) |
| `this-month` | Current month to date | Month start - today | MTD tracking |
| `this-quarter` | Current quarter to date | Quarter start - today | QTD tracking |
| `this-year` | Current year to date | Jan 1 - today | YTD tracking |
| `ytd` | Year to date (alias) | Jan 1 - today | Same as this-year |
| `2024` | Specific year | Jan 1 - Dec 31, 2024 | Historical year |
| `2024-Q1` | Specific quarter | Jan 1 - Mar 31, 2024 | Historical quarter |
| `2024-01` | Specific month | Jan 1 - Jan 31, 2024 | Historical month |
| `all` | All available data | First - last transaction | Complete history |

### Financial Health Score

**Scoring Algorithm** (0-100 scale):

| Factor | Weight | Excellent | Good | Fair | Poor |
|--------|--------|-----------|------|------|------|
| Savings Rate | 30% | ≥20% (30pts) | 10-20% (20pts) | 5-10% (10pts) | <5% (0-9pts) |
| Emergency Fund | 25% | ≥6mo (25pts) | 3-6mo (15pts) | 1-3mo (8pts) | <1mo (0-7pts) |
| Debt-to-Income | 20% | <20% (20pts) | 20-35% (12pts) | 35-50% (5pts) | >50% (0-4pts) |
| Budget Adherence | 15% | <5% var (15pts) | 5-15% var (10pts) | 15-25% var (5pts) | >25% var (0-4pts) |
| Cash Flow Trend | 10% | Positive (10pts) | Neutral (5pts) | Negative (0pts) | Severely negative (0pts) |

**Score Interpretation:**
- 90-100: Excellent - Strong financial health
- 75-89: Good - Solid financial position
- 60-74: Fair - Some areas need improvement
- 40-59: Poor - Significant improvements needed
- 0-39: Critical - Immediate action required

### Examples

```bash
# Comprehensive overview (default 12 months)
/finance analyze --type=overview

# Last 3 months overview
/finance analyze --type=overview --period="last-3-months"

# Current month expenses
/finance analyze --type=expenses --period="this-month"

# Annual income analysis
/finance analyze --type=income --period="2024"

# Year-to-date cash flow
/finance analyze --type=cashflow --period="ytd"

# All-time net worth
/finance analyze --type=networth --period="all"

# Budget comparison (this month)
/finance analyze --type=budget --period="this-month"

# Savings analysis (last 6 months)
/finance analyze --type=savings --period="last-6-months"
```

### Output Example (Overview)

```
Financial Overview (Last 12 Months)
====================================

💰 INCOME
Total Income:                    $84,000.00
Average Monthly Income:          $7,000.00
Income Trend:                    +3.2% YoY

Income Sources:
  Salary (Direct Deposit):       $84,000.00 (100.0%)

💸 EXPENSES
Total Expenses:                  $64,938.00
Average Monthly Expenses:        $5,411.50
Expense Trend:                   +1.8% YoY
Burn Rate:                       $5,411.50/month

Category Breakdown:
  1. Housing                     $25,200.00 (38.8%)  ████████████████████
  2. Food & Dining               $14,694.00 (22.6%)  ███████████
  3. Transportation              $8,460.00  (13.0%)  ███████
  4. Shopping                    $7,553.00  (11.6%)  ██████
  5. Utilities                   $5,057.00  (7.8%)   ████
  6. Entertainment               $2,599.00  (4.0%)   ██
  7. Healthcare                  $1,300.00  (2.0%)   █
  8. Other                       $75.00     (0.1%)

📊 CASH FLOW
Net Cash Flow:                   $19,062.00
Monthly Average:                 $1,588.50
Trend:                           Positive ↗ (+$127/mo)

Cash Flow by Month:
  Jan: +$1,234  Feb: +$1,456  Mar: +$1,589  Apr: +$1,623
  May: +$1,701  Jun: +$1,567  Jul: +$1,890  Aug: +$1,456
  Sep: +$1,623  Oct: +$1,734  Nov: +$1,589  Dec: +$1,600

💵 SAVINGS
Savings Rate:                    22.7%
Annual Savings:                  $19,062.00
Emergency Fund:                  $17,500.00 (3.2 months expenses)
Recommended Emergency Fund:      $32,469.00 (6 months)
Gap to Target:                   $14,969.00

❤️  FINANCIAL HEALTH SCORE:      78/100 (Good)

Score Breakdown:
  ✓ Savings Rate (30pts):        25/30  (Good - 22.7%, target 20%+)
  ⚠ Emergency Fund (25pts):      13/25  (Fair - 3.2mo, target 6mo)
  ✓ Debt-to-Income (20pts):      20/20  (Excellent - minimal debt)
  ✓ Budget Adherence (15pts):    12/15  (Good - minor variances)
  ✓ Cash Flow Trend (10pts):     8/10   (Positive trend)

STRENGTHS:
  ✓ Strong savings rate above 20% target
  ✓ Positive cash flow every month
  ✓ Minimal debt burden
  ✓ Consistent income stream
  ✓ Expenses under control

AREAS TO IMPROVE:
  ⚠ Emergency fund below 6-month target (need $14,969 more)
  ⚠ Discretionary spending at 35% (target <30%)
  ⚠ No investment contributions detected
  ⚠ High housing cost (39% of expenses, target <30%)

RECOMMENDATIONS:
  1. Increase emergency fund by $1,247/month for 12 months
  2. Review discretionary spending (food, shopping, entertainment)
  3. Consider house hacking or roommate to reduce housing costs
  4. Start investing 10-15% of income once emergency fund complete

Next Steps:
  /finance advise --focus="savings"
  /finance project --type=cashflow --months=12
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "No transaction data" | Empty notebook | Import transactions first |
| "Invalid analysis type" | Typo in type | Use valid type from table |
| "Invalid period" | Unrecognized period | Use valid period format |
| "Insufficient data" | Too few transactions for period | Use longer period or import more data |

---

## finance project

**Purpose**: Generate financial projections and forecasts.

### Syntax

```bash
/finance project --type="<projection_type>" [--months=<N>] [--scenario="<scenario>"] [--notebook="<name>"]
```

### Parameters

| Parameter | Type | Required | Default | Description | Valid Values |
|-----------|------|----------|---------|-------------|--------------|
| `--type` | string | Yes | None | Projection type | See Projection Types table |
| `--months` | integer | No | 12 | Number of months to project | 1-360 (30 years) |
| `--scenario` | string | No | `moderate` | Growth scenario | `conservative`, `moderate`, `aggressive` |
| `--notebook` | string | No | Active | Target notebook | Any existing notebook |

### Projection Types

| Type | Description | Required Data | Output | Typical Use |
|------|-------------|---------------|--------|-------------|
| `cashflow` | Monthly income/expense projections | Historical transactions | Monthly projections array | Future planning |
| `savings` | Savings goal progress | Current savings, goal amount | Goal timeline, required contributions | Goal tracking |
| `networth` | Net worth projection | Account balances, growth rates | Future net worth | Wealth tracking |
| `debt` | Debt payoff schedule | Principal, rate, payment | Payoff timeline, total interest | Debt planning |
| `retirement` | Retirement savings | Current savings, contributions | Retirement balance, income | Retirement planning |

### Scenario Parameters

| Scenario | Income Growth | Expense Growth | Investment Return | Risk Level | Use Case |
|----------|---------------|----------------|-------------------|------------|----------|
| `conservative` | 2% annual | 3% annual | 5% annual | Low | Pessimistic planning |
| `moderate` | 4% annual | 3% annual | 7% annual | Medium | Realistic planning (default) |
| `aggressive` | 6% annual | 2% annual | 10% annual | High | Optimistic planning |

### Months Parameter

| Range | Purpose | Example |
|-------|---------|---------|
| 1-3 | Short-term planning | Next quarter |
| 6-12 | Medium-term planning | Annual budget (default) |
| 24-36 | Long-term goals | House down payment |
| 120-360 | Retirement planning | 10-30 year projection |

### Projection-Specific Parameters

**Savings Goal Parameters** (additional):
- `--goal-amount=<number>` - Target savings amount
- `--target-date=<YYYY-MM-DD>` - Goal deadline
- `--monthly-contribution=<number>` - Expected monthly savings
- `--annual-return=<float>` - Expected return rate (default: 0.05)

**Debt Payoff Parameters** (additional):
- `--principal=<number>` - Loan principal amount
- `--interest-rate=<float>` - Annual interest rate (e.g., 0.05 for 5%)
- `--monthly-payment=<number>` - Monthly payment amount

**Retirement Parameters** (additional):
- `--current-age=<number>` - Your current age
- `--retirement-age=<number>` - Target retirement age (default: 65)
- `--current-savings=<number>` - Current retirement savings
- `--monthly-contribution=<number>` - Monthly contribution
- `--expected-return=<float>` - Annual return rate (default: 0.07)

### Examples

```bash
# 12-month cash flow (moderate scenario)
/finance project --type=cashflow --months=12

# Conservative 24-month projection
/finance project --type=cashflow --months=24 --scenario="conservative"

# Aggressive 5-year projection
/finance project --type=cashflow --months=60 --scenario="aggressive"

# Savings goal: $50k in 2 years
/finance project --type=savings --goal-amount=50000 --months=24 --monthly-contribution=2000

# Debt payoff: $25k loan at 5% APR, $500/mo payment
/finance project --type=debt --principal=25000 --interest-rate=0.05 --monthly-payment=500

# Retirement planning: 30-year projection
/finance project --type=retirement --months=360 --current-age=35 --retirement-age=65 \
  --current-savings=50000 --monthly-contribution=500 --expected-return=0.07

# Net worth projection (3 years)
/finance project --type=networth --months=36 --scenario="moderate"
```

### Output Example (Cash Flow Projection)

```
12-Month Cash Flow Projection
==============================

Scenario: Moderate
Base Data: Last 12 months average
Projection Period: Feb 2025 - Jan 2026

Assumptions:
  Base Monthly Income:     $7,000.00
  Income Growth Rate:      4.0% annually (0.33% monthly)
  Base Monthly Expenses:   $5,411.50
  Expense Growth Rate:     3.0% annually (0.25% monthly)
  Starting Date:           2025-02-01

Monthly Projections:
┌───────┬───────────┬────────────┬─────────────┬──────────────┐
│ Month │   Income  │  Expenses  │  Cash Flow  │  Cumulative  │
├───────┼───────────┼────────────┼─────────────┼──────────────┤
│ Feb25 │  $7,023.10│  $5,425.53 │  $1,597.57  │   $1,597.57  │
│ Mar25 │  $7,046.33│  $5,439.09 │  $1,607.24  │   $3,204.81  │
│ Apr25 │  $7,069.69│  $5,452.68 │  $1,617.01  │   $4,821.82  │
│ May25 │  $7,093.17│  $5,466.31 │  $1,626.86  │   $6,448.68  │
│ Jun25 │  $7,116.78│  $5,479.97 │  $1,636.81  │   $8,085.49  │
│ Jul25 │  $7,140.51│  $5,493.67 │  $1,646.84  │   $9,732.33  │
│ Aug25 │  $7,164.37│  $5,507.40 │  $1,656.97  │  $11,389.30  │
│ Sep25 │  $7,188.36│  $5,521.16 │  $1,667.20  │  $13,056.50  │
│ Oct25 │  $7,212.47│  $5,534.96 │  $1,677.51  │  $14,734.01  │
│ Nov25 │  $7,236.71│  $5,548.79 │  $1,687.92  │  $16,421.93  │
│ Dec25 │  $7,261.07│  $5,562.66 │  $1,698.41  │  $18,120.34  │
│ Jan26 │  $7,285.56│  $5,576.56 │  $1,709.00  │  $19,829.34  │
└───────┴───────────┴────────────┴─────────────┴──────────────┘

Summary Statistics:
  Projected Annual Income:     $86,838.12  (+3.4% from current)
  Projected Annual Expenses:   $66,008.78  (+1.7% from current)
  Projected Annual Savings:    $20,829.34  (+9.3% from current)
  Average Monthly Surplus:     $1,735.78
  Projected Savings Rate:      24.0%

Insights:
  ✓ Positive cash flow every month
  ✓ Growing monthly surplus over time
  ✓ On track to exceed 20% savings rate target
  ✓ Income growing faster than expenses (good trend)

Scenario Comparison:
  Conservative:  $18,234.56 annual savings (-12.5%)
  Moderate:      $20,829.34 annual savings (baseline)
  Aggressive:    $23,892.10 annual savings (+14.7%)

Recommendation:
  Based on moderate scenario, you can expect to save $20,829 over the next 12 months.
  This supports building emergency fund to 6 months within 9 months.

Next Steps:
  /finance advise --focus="savings" --goal="Build emergency fund"
  /finance report --type="projections" --period="next-12-months"
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "Insufficient historical data" | Need 3+ months | Import more transactions |
| "Invalid months value" | Out of range 1-360 | Use valid month count |
| "Missing required parameter" | Savings/debt params missing | Provide all required params for type |
| "Invalid interest rate" | Rate < 0 or > 1 | Use decimal (0.05 for 5%) |

---

## finance advise

**Purpose**: Get AI-driven financial recommendations and personalized action plans.

### Syntax

```bash
/finance advise [--focus="<area>"] [--goal="<objective>"] [--notebook="<name>"]
```

### Parameters

| Parameter | Type | Required | Default | Description | Valid Values |
|-----------|------|----------|---------|-------------|--------------|
| `--focus` | string | No | `overall` | Focus area for recommendations | See Focus Areas table |
| `--goal` | string | No | None | Specific financial goal | Free text |
| `--notebook` | string | No | Active | Target notebook | Any existing notebook |

### Focus Areas

| Focus Area | Description | Analysis Performed | Recommendation Types |
|------------|-------------|-------------------|---------------------|
| `overall` | Comprehensive advice | All financial metrics | Budget, savings, debt, investments, goals |
| `budget` | Budget optimization | Category spending, variance | Spending cuts, reallocation, efficiency |
| `savings` | Savings acceleration | Savings rate, emergency fund | Increase income, reduce expenses, automation |
| `debt` | Debt reduction | Debt-to-income, interest rates | Payoff strategies, refinancing, consolidation |
| `spending` | Spending improvements | Category patterns, trends | Habit changes, subscriptions, alternatives |
| `goals` | Goal planning | Goal feasibility, timeline | Adjusted targets, strategies, milestones |

### Recommendation Structure

Each recommendation includes:

| Component | Description | Example |
|-----------|-------------|---------|
| **Priority** | High/Medium/Low | 🔴 High, 🟡 Medium, 🟢 Low |
| **Insight** | What was observed | "Current savings rate: 15%" |
| **Recommendation** | Suggested action | "Increase to 20% by reducing dining out" |
| **Action Items** | Specific steps | "1. Meal prep Sundays, 2. Limit dining to 2x/week" |
| **Impact** | Expected outcome | "Save $430/month = $5,160/year" |
| **Effort** | Implementation difficulty | Easy/Moderate/Difficult |
| **Timeline** | When to implement | Immediate/This month/This quarter |

### Examples

```bash
# Comprehensive financial advice
/finance advise

# Budget optimization recommendations
/finance advise --focus="budget"

# Savings acceleration strategies
/finance advise --focus="savings"

# Debt reduction guidance
/finance advise --focus="debt"

# Spending pattern improvements
/finance advise --focus="spending"

# Goal-specific advice
/finance advise --focus="goals" --goal="Save $50k for house down payment"

# Savings with specific goal
/finance advise --focus="savings" --goal="Build 6-month emergency fund"

# Overall advice for specific notebook
/finance advise --notebook="2024-review"
```

### Output Example

```
AI Financial Recommendations
=============================

Analysis Date: 2025-01-28
Focus: Savings Acceleration
Goal: Build 6-month emergency fund

Current Financial Snapshot:
  Monthly Income:          $7,000.00
  Monthly Expenses:        $5,411.50
  Current Savings Rate:    22.7%
  Emergency Fund:          $17,500 (3.2 months)
  Target Emergency Fund:   $32,472 (6 months)
  Gap to Target:           $14,972

═══════════════════════════════════════════════════════════════

🔴 PRIORITY 1: Build Emergency Fund to 6 Months

Current:   $17,500 (3.2 months of expenses)
Target:    $32,472 (6 months of expenses)
Shortfall: $14,972

Timeline & Strategy:
  Option A: Aggressive (9 months)
    Monthly allocation: $1,664
    Completion date: October 2025
    Requires: $1,076 in spending cuts + $588 current surplus

  Option B: Moderate (12 months)
    Monthly allocation: $1,248
    Completion date: January 2026
    Requires: $660 in spending cuts + $588 current surplus

  Option C: Conservative (18 months)
    Monthly allocation: $832
    Completion date: July 2026
    Requires: $244 in spending cuts + $588 current surplus

Recommended: Option B (12-month timeline)

Action Items:
  ☐ Open high-yield savings account (5%+ APY)
    Recommended: Marcus, Ally, Capital One 360
    Benefit: Earn $800+ in interest over 12 months

  ☐ Set up automatic monthly transfer: $1,248
    Day of month: Day after paycheck
    From: Checking → To: HYSA Emergency Fund

  ☐ Find $660/month in spending reductions (see Priorities 2-4)

  ☐ Track progress monthly
    Review date: Last day of each month
    Milestone rewards: Every $5,000 increment

Expected Outcome:
  ✓ Fully funded emergency fund by January 2026
  ✓ Financial resilience for 6+ months unemployment
  ✓ Reduced financial stress and anxiety
  ✓ Foundation for other financial goals

─────────────────────────────────────────────────────────────────

🟡 PRIORITY 2: Optimize Food & Dining Budget

Current Spending:    $1,224.50/month (22.6% of expenses)
Benchmark:           $541-$812/month (10-15% of expenses)
Over Budget:         $412-$684/month
Potential Savings:   $430/month ($5,160/year)

Breakdown:
  Groceries:          $687/month (56%)  ← On track
  Dining Out:         $389/month (32%)  ← High
  Delivery/Takeout:   $148/month (12%)  ← High

Specific Actions:

  ☐ Meal Prep Sundays (Save ~$120/month)
    What: Cook 5 dinners every Sunday
    Time: 2-3 hours weekly
    Benefit: Reduces weekday takeout from $15 → $5
    Tools: Meal prep containers, recipes

  ☐ Reduce Dining Out to 2x/Week (Save ~$180/month)
    Current: ~6 times/week at $30/meal
    Target: 2 times/week (weekend social)
    Replace: Home-cooked meals + meal prep
    Benefit: Save $720/month, healthier eating

  ☐ Cancel/Reduce Delivery Services (Save ~$80/month)
    DoorDash/UberEats: $148/month
    Strategy: Pick up orders (no delivery fee)
    Or: Cook at home instead

  ☐ Use Grocery Cashback Apps (Save ~$50/month)
    Apps: Ibotta, Fetch Rewards, Checkout 51
    Effort: Scan receipts (2 min/week)
    Return: 3-5% cash back on groceries

Total Monthly Savings: $430
Annual Impact: $5,160
Effort Level: Moderate (requires habit change)
Success Rate: 85% with meal prep commitment

─────────────────────────────────────────────────────────────────

🟡 PRIORITY 3: Audit & Optimize Subscriptions

Current Subscriptions: 8 services
Monthly Cost: $157.00
Annual Cost: $1,884.00

Subscription Analysis:
┌─────────────────────┬─────────┬────────────┬──────────────┐
│ Service             │  Cost   │   Usage    │ Recommendation│
├─────────────────────┼─────────┼────────────┼──────────────┤
│ Premium Gym         │  $89/mo │ 1.2x/week  │ 🔴 Downgrade  │
│ Netflix Premium     │  $20/mo │ Daily      │ ✓ Keep       │
│ Hulu + Live TV      │  $15/mo │ Weekly     │ ⚠ Consider   │
│ Spotify Premium     │  $11/mo │ Daily      │ ✓ Keep       │
│ Amazon Prime        │  $15/mo │ 2x/month   │ ⚠ Consider   │
│ Audible             │  $15/mo │ 0.5x/month │ 🔴 Cancel    │
│ Cloud Storage       │   $3/mo │ Active     │ ✓ Keep       │
│ News Subscription   │   $9/mo │ Rarely     │ 🔴 Cancel    │
└─────────────────────┴─────────┴────────────┴──────────────┘

Recommended Changes:

  ☐ Gym: Premium → Basic ($89 → $30)
    Rationale: Low usage (1.2x/week)
    Alternative: Basic gym or home workouts
    Savings: $59/month

  ☐ Audible: Cancel ($15 → $0)
    Rationale: 0.5 books/month = $30/book
    Alternative: Library app (Libby) - FREE
    Savings: $15/month

  ☐ News: Cancel ($9 → $0)
    Rationale: Rarely used
    Alternative: Free news websites
    Savings: $9/month

  ☐ Streaming: Rotate services
    Strategy: Keep Netflix, rotate Hulu quarterly
    Benefit: Always have fresh content
    Savings: $10/month average

Total Monthly Savings: $93
Annual Impact: $1,116
Effort Level: Easy (one-time cancellations)

─────────────────────────────────────────────────────────────────

💡 QUICK WIN: Increase 401(k) to Capture Full Match

Current Contribution: 3% ($210/month)
Employer Match: Up to 5% (free money!)
Recommended: 5% ($350/month)

Impact:
  Your contribution: +$140/month
  Employer match: +$140/month (FREE)
  Total retirement: +$280/month
  Annual benefit: $3,360 ($1,680 free + $1,680 tax savings)

Action: Update 401(k) contribution in HR portal

─────────────────────────────────────────────────────────────────

📊 COMBINED IMPACT SUMMARY

Monthly Savings Potential:
  Food & Dining optimization:  $430
  Subscription cuts:           $93
  Total:                       $523

Applied to Emergency Fund Goal:
  Current timeline:           12 months ($1,248/month)
  With optimizations:         9.5 months ($1,576/month)
  Time saved:                 2.5 months

Alternative Allocation:
  Emergency fund (70%):       $366 → Full funding in 11 months
  401(k) increase (15%):      $78  → Extra retirement savings
  Fun money (15%):            $79  → Guilt-free spending

═══════════════════════════════════════════════════════════════

📋 IMPLEMENTATION PLAN

Week 1 (Immediate Actions):
  ☐ Open high-yield savings account
  ☐ Set up automatic $1,248 monthly transfer
  ☐ Cancel Audible subscription
  ☐ Cancel news subscription
  ☐ Downgrade gym membership

Week 2 (Habit Changes):
  ☐ Start Sunday meal prep routine
  ☐ Download grocery cashback apps
  ☐ Plan dining out schedule (2x/week)

Month 2 (Review & Adjust):
  ☐ Track actual spending changes
  ☐ Adjust if needed
  ☐ Celebrate first $1,248 saved!

Monthly Check-ins:
  Last day of each month:
    ☐ Verify $1,248 deposited to emergency fund
    ☐ Review spending vs. targets
    ☐ Adjust strategies as needed

═══════════════════════════════════════════════════════════════

⚠️  DISCLAIMER

This AI-generated advice is for informational purposes only and does
not constitute professional financial planning advice. Consider consulting
a certified financial planner for personalized guidance tailored to your
complete financial situation, goals, and risk tolerance.

═══════════════════════════════════════════════════════════════

Next Steps:
  /finance project --type=savings --goal-amount=32472 --months=9
  /finance analyze --type=budget --period="this-month"
  /finance report --type="categories" --period="last-3-months"
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "Insufficient data for advice" | No transactions or analysis | Import data and run analysis first |
| "Invalid focus area" | Typo in focus | Use valid focus from table |
| "No active notebook" | No notebook selected | Specify --notebook or run init |

---

## finance report

**Purpose**: Create visualizations and charts from financial data.

### Syntax

```bash
/finance report --type="<chart_type>" [--period="<time_range>"] [--format="<output>"] [--notebook="<name>"]
```

### Parameters

| Parameter | Type | Required | Default | Description | Valid Values |
|-----------|------|----------|---------|-------------|--------------|
| `--type` | string | Yes | None | Type of visualization | See Chart Types table |
| `--period` | string | No | `last-12-months` | Time range | Same as analyze periods |
| `--format` | string | No | `inline` | Output format | `inline`, `png`, `pdf` |
| `--notebook` | string | No | Active | Target notebook | Any existing notebook |

### Chart Types

| Type | Visualization | Purpose | Data Required | Output |
|------|---------------|---------|---------------|--------|
| `income-expense` | Line/bar chart | Track income vs expenses over time | Transactions | Trend chart with net cash flow |
| `categories` | Pie chart | Spending breakdown | Categorized transactions | Category percentages |
| `networth` | Area chart | Net worth trend | Account balances over time | Stacked area chart |
| `cashflow` | Waterfall chart | Income/expense flow | Monthly aggregations | Waterfall visualization |
| `budget` | Grouped bar chart | Budget vs actual | Budget and transactions | Comparison bars with variance |
| `projections` | Line chart with bands | Future projections | Projection data | Forecast with confidence intervals |
| `dashboard` | Multi-chart layout | Comprehensive overview | All data | Combined visualization |

### Output Formats

| Format | Description | File Location | Use Case |
|--------|-------------|---------------|----------|
| `inline` | Display in notebook | Notebook output cell | Interactive analysis (default) |
| `png` | PNG image file | `.claude/finance-notebooks/reports/<name>.png` | Sharing, presentations |
| `pdf` | PDF document | `.claude/finance-notebooks/reports/<name>.pdf` | Printing, archiving |

### Chart Specifications

**Income-Expense Trend:**
- X-axis: Time (months)
- Y-axis: Amount ($)
- Series: Income (green bars), Expenses (red bars), Net Cash Flow (blue line)
- Features: Grid lines, legend, currency formatting

**Category Breakdown:**
- Chart: Pie or donut chart
- Slices: Top 10 categories + "Other"
- Labels: Category name, percentage, amount
- Colors: Distinct colors per category

**Net Worth Trend:**
- X-axis: Time (months)
- Y-axis: Net Worth ($)
- Areas: Assets (green), Liabilities (red), Net Worth (line)
- Features: Stacked area, trend line

**Cash Flow Waterfall:**
- Bars: Income sources (up), Expense categories (down)
- Colors: Green (income), Red (expenses), Blue (net)
- Labels: Category, amount

**Budget Comparison:**
- X-axis: Categories
- Y-axis: Amount ($)
- Bars: Budget (gray), Actual (color-coded)
- Features: Variance labels, over/under indicators

**Projections:**
- X-axis: Future months
- Y-axis: Amount ($)
- Lines: Conservative, Moderate, Aggressive scenarios
- Bands: Confidence intervals
- Features: Historical data reference line

### Examples

```bash
# Income vs expense trend (last 12 months, inline)
/finance report --type="income-expense"

# Category breakdown (last 3 months, inline)
/finance report --type="categories" --period="last-3-months"

# Net worth trend (all time, export PNG)
/finance report --type="networth" --period="all" --format="png"

# Cash flow waterfall (this month)
/finance report --type="cashflow" --period="this-month"

# Budget comparison (export PDF)
/finance report --type="budget" --period="this-month" --format="pdf"

# Projections chart (next 12 months)
/finance report --type="projections" --period="next-12-months"

# Comprehensive dashboard
/finance report --type="dashboard" --period="last-12-months" --format="pdf"
```

### Output

```
✓ Generated report: income-expense trend
✓ Period: Last 12 months (Feb 2024 - Jan 2025)
✓ Data points: 12 months
✓ Format: inline (displayed in notebook)

Chart Details:
  Type: Income vs Expense Trend
  Income Range: $6,800 - $7,200
  Expense Range: $5,200 - $5,600
  Net Cash Flow Range: $1,200 - $1,800
  Trend: Positive (increasing savings)

File saved: .claude/finance-notebooks/reports/income-expense-2024-2025.png
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "No data for period" | Empty date range | Import data for period or use different period |
| "Invalid chart type" | Typo | Use valid chart type from table |
| "Visualization library not found" | Missing matplotlib | `pip install matplotlib seaborn` |
| "Cannot export" | Permission issue | Check write permissions in reports/ directory |

---

## finance list

**Purpose**: List all financial notebooks with metadata.

### Syntax

```bash
/finance list
```

### Parameters

None - this command takes no parameters.

### Output Format

```
Financial Notebooks
===================

Active Notebook: 2025-budget ✓

Available Notebooks:
┌────┬─────────────────────────┬──────────────┬───────────────────┬───────────┬──────────┐
│ #  │ Notebook Name           │ Created      │ Last Modified     │ Size      │ Status   │
├────┼─────────────────────────┼──────────────┼───────────────────┼───────────┼──────────┤
│ 1  │ 2025-budget.ipynb       │ 2025-01-01   │ 2025-01-28 10:45  │ 245 KB    │ Active   │
│ 2  │ 2024-annual.ipynb       │ 2024-01-01   │ 2024-12-31 17:30  │ 512 KB    │ Archived │
│ 3  │ 2025-Q1.ipynb           │ 2025-01-15   │ 2025-01-20 14:20  │ 128 KB    │ Inactive │
│ 4  │ house-fund.ipynb        │ 2024-06-01   │ 2025-01-15 09:00  │ 189 KB    │ Inactive │
└────┴─────────────────────────┴──────────────┴───────────────────┴───────────┴──────────┘

Total: 4 notebooks
Storage: .claude/finance-notebooks/
Total Size: 1.07 MB

Legend:
  Active:   Currently connected and available for commands
  Inactive: Available but not currently active
  Archived: Older notebook, marked for archival

Commands:
  Use notebook:    /finance init --notebook="name" (without .ipynb)
  Analyze:         /finance analyze --notebook="2025-budget"
  Delete:          /finance delete --notebook="old-notebook"
```

### Metadata Displayed

| Field | Description | Example |
|-------|-------------|---------|
| # | Sequential number | 1, 2, 3 |
| Notebook Name | File name with extension | 2025-budget.ipynb |
| Created | Creation date | 2025-01-01 |
| Last Modified | Last save timestamp | 2025-01-28 10:45 |
| Size | File size | 245 KB |
| Status | Active/Inactive/Archived | Active ✓ |

### Status Indicators

| Status | Symbol | Meaning |
|--------|--------|---------|
| Active | ✓ | Currently connected kernel |
| Inactive | - | Notebook exists but not active |
| Archived | 📦 | Marked for archival |

### Examples

```bash
# List all notebooks
/finance list
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "No notebooks found" | Empty directory | Create notebook with /finance init |
| "jupyter-mcp unavailable" | MCP not running | Start jupyter-mcp server |

---

## finance delete

**Purpose**: Delete a financial notebook (creates backup before deletion).

### Syntax

```bash
/finance delete --notebook="<notebook_name>" [--confirm]
```

### Parameters

| Parameter | Type | Required | Default | Description | Valid Values |
|-----------|------|----------|---------|-------------|--------------|
| `--notebook` | string | Yes | None | Notebook name to delete | Existing notebook name |
| `--confirm` | flag | No | false | Skip confirmation prompt | No value needed (flag) |

### Deletion Process

| Step | Action | Details |
|------|--------|---------|
| 1 | Validate | Check notebook exists |
| 2 | Show info | Display notebook details for confirmation |
| 3 | Confirm | Prompt user (unless --confirm flag) |
| 4 | Backup | Create backup in `.backups/` directory |
| 5 | Disconnect | Close notebook if active |
| 6 | Delete | Remove .ipynb file |
| 7 | Confirm | Show deletion success and backup location |

### Backup Location

Backups are stored with timestamp:
```
.claude/finance-notebooks/.backups/<notebook-name>-<timestamp>.ipynb
```

Example: `2024-budget-20250128-143052.ipynb`

### Examples

```bash
# Delete with confirmation prompt
/finance delete --notebook="old-budget"

# Delete without confirmation (use with caution!)
/finance delete --notebook="test-notebook" --confirm

# Delete specific notebook
/finance delete --notebook="2023-annual"
```

### Output (with confirmation)

```
⚠️  WARNING: Permanent Deletion

You are about to delete the following notebook:

  Notebook:       old-budget.ipynb
  Created:        2024-01-01
  Last Modified:  2024-12-31 17:30
  Size:           512 KB
  Transactions:   1,247
  Status:         Inactive

A backup will be created before deletion.
This action cannot be undone (except via backup restore).

Type 'yes' to confirm deletion: yes

✓ Creating backup...
✓ Backup created: .claude/finance-notebooks/.backups/old-budget-20250128-143052.ipynb
✓ Disconnecting from notebook...
✓ Deleting notebook file...
✓ Notebook deleted successfully

Backup Location:
  .claude/finance-notebooks/.backups/old-budget-20250128-143052.ipynb

To restore this notebook:
  cp .claude/finance-notebooks/.backups/old-budget-20250128-143052.ipynb \
     .claude/finance-notebooks/old-budget.ipynb
```

### Output (with --confirm flag)

```
✓ Creating backup...
✓ Backup created: .claude/finance-notebooks/.backups/test-20250128-143100.ipynb
✓ Notebook deleted: test.ipynb
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "Notebook not found" | Invalid name | Check with `/finance list` |
| "Cannot delete active notebook" | Trying to delete current notebook | Switch to different notebook first |
| "Backup failed" | Permission issue | Check write permissions |
| "User cancelled" | Typed 'no' at confirmation | Normal cancellation |

---

## Additional Reference

### Global Options

These options work with all commands (where applicable):

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--notebook="name"` | string | Active | Target notebook for operation |
| `--help` | flag | false | Show command help |
| `--verbose` | flag | false | Show detailed output |
| `--quiet` | flag | false | Minimal output (errors only) |

### Common Parameters

**Time Periods** (for analyze, report):
- `last-month`, `last-3-months`, `last-6-months`, `last-12-months`
- `this-month`, `this-quarter`, `this-year`, `ytd`
- `2024`, `2024-Q1`, `2024-01`
- `all`

**Account Types** (for import):
- `checking`, `savings`, `credit`, `cash`, `investment`

**Scenarios** (for project):
- `conservative`, `moderate`, `aggressive`

**Output Formats** (for report):
- `inline`, `png`, `pdf`

### Data Requirements

| Command | Minimum Data Required | Recommended Data |
|---------|----------------------|------------------|
| `init` | None | None |
| `import` | CSV/Excel file | 1+ month of transactions |
| `analyze` | 10+ transactions | 3+ months of transactions |
| `project` | 3+ months history | 6-12 months history |
| `advise` | Analysis data | 6+ months of history |
| `report` | Transaction data | 3+ months for trends |
| `list` | None | None |
| `delete` | Notebook exists | Backup before delete |

### Best Practices

1. **Start with init**: Always create notebook first
2. **Import regularly**: Weekly or monthly imports
3. **Analyze monthly**: Review finances at month-end
4. **Project quarterly**: Review forecasts every 3 months
5. **Get advice**: Run advise after major life changes
6. **Visualize trends**: Create reports for insights
7. **Archive yearly**: Delete or archive old notebooks annually
8. **Backup data**: Notebooks are gitignored, backup separately

### Quick Reference Card

```
QUICK COMMAND REFERENCE
=======================

Create Notebook:    /finance init --notebook="2025-budget"
Import Data:        /finance import --source="file.csv" --type="checking"
Analyze:            /finance analyze --type=overview
Project:            /finance project --type=cashflow --months=12
Get Advice:         /finance advise --focus="savings"
Create Report:      /finance report --type="income-expense"
List Notebooks:     /finance list
Delete:             /finance delete --notebook="old"

COMMON WORKFLOWS
================

Monthly Review:
  /finance import --source="month.csv" --type="checking"
  /finance analyze --type=overview --period="this-month"
  /finance analyze --type=budget --period="this-month"

Annual Planning:
  /finance init --notebook="2025-plan"
  /finance import --source="2024-all.csv"
  /finance analyze --type=overview --period="2024"
  /finance project --type=cashflow --months=12
  /finance advise --focus="goals"

Emergency Fund Goal:
  /finance analyze --type=savings
  /finance project --type=savings --goal-amount=30000 --months=12
  /finance advise --focus="savings" --goal="Emergency fund"

DATA FORMATS
============

CSV Required Columns:  date, description, amount
Supported Date Formats: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY
Account Types:         checking, savings, credit, cash, investment
Time Periods:          last-N-months, this-month/quarter/year, YYYY, all

HELP & SUPPORT
==============

Documentation:  docs/finance/QUICK_START.md
Command Ref:    docs/finance/COMMAND_REFERENCE.md
Import Guide:   .claude/finance-notebooks/IMPORT_GUIDE.md
Full Manual:    docs/finance/MANUAL.md (this file)
```

---

**End of Manual**

For additional help:
- Quick Start: `docs/finance/QUICK_START.md`
- Command Reference: `docs/finance/COMMAND_REFERENCE.md`
- Troubleshooting: `docs/finance/TROUBLESHOOTING.md`
- API Reference: `docs/finance/API_REFERENCE.md`
