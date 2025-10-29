# Personal Finance Advisor

AI-powered personal finance management using Jupyter notebooks via the `/finance` command.

## Overview

The Personal Finance Advisor provides comprehensive financial analysis, projections, and AI-driven recommendations through interactive Jupyter notebooks. All data stays local for complete privacy.

## Quick Links

- **[Quick Start Guide](finance/QUICK_START.md)** - Get started in 10 minutes
- **[Command Reference](finance/COMMAND_REFERENCE.md)** - Complete command documentation
- **[Privacy & Security](finance/PRIVACY_SECURITY.md)** - Data protection practices

## Features

### 📊 Financial Analysis
- Income vs. expense tracking
- Net worth calculation
- Cash flow analysis
- Savings metrics
- Budget vs. actual comparisons
- Financial health scoring (0-100)

### 📈 Projections & Forecasting
- 12-month cash flow projections
- Savings goal tracking
- Retirement planning
- Debt payoff schedules
- Scenario modeling (conservative/moderate/aggressive)

### 🎨 Visualizations
- Income/expense trend charts
- Category spending breakdowns
- Net worth tracking
- Budget comparison graphs
- Projection visualizations

### 🤖 AI Advisory
- Context-aware recommendations
- Budget optimization
- Savings strategies
- Debt reduction guidance
- Spending insights

## Quick Start

```bash
# 1. Create notebook
/finance init --notebook="2025-budget"

# 2. Import transactions
/finance import --source="transactions.csv" --type="checking"

# 3. Analyze finances
/finance analyze --type=overview

# 4. Get recommendations
/finance advise --focus="savings"

# 5. Create visualizations
/finance report --type="income-expense"
```

## Commands

| Command | Parameters | Description | Example |
|---------|------------|-------------|---------|
| `/finance init` | `--notebook="name"` | Create new financial notebook with template structure | `/finance init --notebook="2025-budget"` |
| `/finance import` | `--source="path"` `--type="account"` | Import transactions from CSV/Excel (checking, savings, credit, cash) | `/finance import --source="transactions.csv" --type="checking"` |
| `/finance analyze` | `--type="analysis"` `--period="range"` | Analyze finances (overview, income, expenses, cashflow, networth, savings, budget) | `/finance analyze --type=overview --period="last-3-months"` |
| `/finance project` | `--type="projection"` `--months=N` `--scenario="name"` | Generate forecasts (cashflow, savings, networth, debt, retirement) | `/finance project --type=cashflow --months=12 --scenario="moderate"` |
| `/finance advise` | `--focus="area"` `--goal="objective"` | Get AI recommendations (overall, budget, savings, debt, spending, goals) | `/finance advise --focus="savings" --goal="Emergency fund"` |
| `/finance report` | `--type="chart"` `--period="range"` `--format="output"` | Create visualizations (income-expense, categories, networth, cashflow, budget, projections) | `/finance report --type="income-expense" --period="last-12-months"` |
| `/finance list` | None | List all financial notebooks with metadata | `/finance list` |
| `/finance delete` | `--notebook="name"` `--confirm` | Delete a notebook (creates backup) | `/finance delete --notebook="old-budget" --confirm` |

## Requirements

- Claude Code with jupyter-mcp server
- Python 3.8+ with pandas, numpy, matplotlib
- Transaction data in CSV or Excel format

## Privacy & Security

🔒 **All financial data stays local:**
- Notebooks stored in `.claude/finance-notebooks/` (gitignored)
- No external API calls for sensitive data
- All processing via local jupyter-mcp server
- Optional encryption for backups

## Importing Bank Statements

### Where to Store Bank Statements

**Recommended Location:** `~/Documents/Finance/statements/`

```bash
mkdir -p ~/Documents/Finance/statements
mkdir -p ~/Documents/Finance/archives
```

### Method 1: Direct Import (CSV/Excel)

```bash
# Single file
/finance import --source="~/Documents/Finance/checking.csv" --type="checking"

# Delete after import for security
rm ~/Documents/Finance/checking.csv
```

### Method 2: Consolidate Multiple Files

Use the built-in consolidation tool to combine multiple statements:

```bash
cd .claude/finance-notebooks

# Combine multiple CSV/Excel files
python consolidate_statements.py \
  ~/Documents/Finance/checking-*.csv \
  -o ~/Documents/Finance/combined-2024.csv

# Import the combined file
/finance import --source="~/Documents/Finance/combined-2024.csv" --type="checking"
```

**Features:**
- ✅ Combines multiple CSV/Excel files
- ✅ Removes duplicates automatically
- ✅ Sorts transactions by date
- ✅ Standardizes column names

### Method 3: Extract from PDF Statements

For PDF bank statements, use the extraction tool:

```bash
# Install PDF tools (one-time setup)
pip install pdfplumber pandas

# Extract transactions from PDFs
cd .claude/finance-notebooks
python extract_pdf_statements.py \
  ~/Documents/Finance/*.pdf \
  -o ~/Documents/Finance/extracted.csv

# Import the extracted data
/finance import --source="~/Documents/Finance/extracted.csv" --type="checking"
```

**Features:**
- ✅ Extracts transaction tables from PDFs
- ✅ Handles multiple PDFs at once
- ✅ Auto-detects transaction columns
- ✅ Removes duplicates

### Import Helper Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| `consolidate_statements.py` | Combine multiple CSV/Excel files | `python consolidate_statements.py file1.csv file2.csv -o combined.csv` |
| `extract_pdf_statements.py` | Extract transactions from PDF statements | `python extract_pdf_statements.py statement.pdf -o transactions.csv` |
| `IMPORT_GUIDE.md` | Complete import documentation | See `.claude/finance-notebooks/IMPORT_GUIDE.md` |

### Supported Data Formats

**CSV/Excel Requirements:**
- Required columns: `date`, `description`, `amount`
- Optional columns: `category`, `account`, `balance`

**Supported Date Formats:**
- `2025-01-15` (YYYY-MM-DD)
- `01/15/2025` (MM/DD/YYYY)
- `15/01/2025` (DD/MM/YYYY)
- `Jan 15, 2025`

**Account Types:**
- `checking` - Checking accounts
- `savings` - Savings accounts
- `credit` - Credit cards
- `cash` - Cash transactions
- `investment` - Investment accounts

### Complete Import Workflow

```bash
# 1. Download statements from bank to ~/Documents/Finance/

# 2. If PDF, extract first
python extract_pdf_statements.py ~/Documents/Finance/*.pdf -o ~/Documents/Finance/all.csv

# 3. Create notebook and import
/finance init --notebook="2025-budget"
/finance import --source="~/Documents/Finance/all.csv" --type="checking"

# 4. Delete source files (data now in gitignored notebook)
rm ~/Documents/Finance/all.csv

# 5. Analyze
/finance analyze --type=overview
```

### Security Best Practices

🔒 **Always delete source files after import:**
- Imported data is stored in gitignored notebooks
- Source CSV/Excel/PDF files should be deleted
- Or move to encrypted archive location

🔒 **Never commit financial data to git:**
- `.gitignore` already configured for `.ipynb`, `.csv`, `.xlsx`, `.pdf`
- All notebooks in `.claude/finance-notebooks/` are gitignored
- Run `git status` to verify no financial files are staged

## Architecture

```
.claude/
├── commands/
│   └── finance.md              # Main command definition
├── finance-notebooks/          # Notebook storage (gitignored)
│   ├── .gitignore             # Privacy protection
│   ├── README.md              # Storage documentation
│   ├── finance_utils.py       # Helper function library
│   └── *.ipynb                # Your notebooks (gitignored)
└── templates/
    └── FINANCE_NOTEBOOK_TEMPLATE.md  # Notebook structure

docs/finance/
├── QUICK_START.md             # Getting started guide
├── COMMAND_REFERENCE.md       # Complete command docs
├── TUTORIALS.md               # Step-by-step guides
├── API_REFERENCE.md           # Developer documentation
├── TROUBLESHOOTING.md         # Common issues
└── PRIVACY_SECURITY.md        # Security practices
```

## Use Cases

### Monthly Budget Tracking
Track income and expenses, compare to budget, identify savings opportunities.

### Financial Goal Planning
Set savings goals, project timeline, get strategies to accelerate progress.

### Retirement Planning
Project retirement savings, calculate required contributions, model scenarios.

### Debt Reduction
Create payoff schedules, optimize payment strategies, track progress.

### Net Worth Tracking
Monitor assets and liabilities over time, visualize growth trends.

## Example Workflows

### Monthly Review
```bash
/finance import --source="jan2025.csv"
/finance analyze --type=overview --period="this-month"
/finance report --type="categories"
/finance advise --focus="budget"
```

### Annual Planning
```bash
/finance init --notebook="2025-plan"
/finance import --source="2024-all.csv"
/finance analyze --type=overview --period="2024"
/finance project --type=cashflow --months=12
/finance advise --focus="goals"
```

### Financial Health Check
```bash
/finance analyze --type=overview
/finance analyze --type=savings
/finance report --type="networth" --period="all"
/finance advise --focus="overall"
```

## Documentation

- **[Quick Start Guide](finance/QUICK_START.md)** - Get up and running
- **[Command Reference](finance/COMMAND_REFERENCE.md)** - Detailed command docs
- **[Tutorials](finance/TUTORIALS.md)** - Step-by-step examples
- **[API Reference](finance/API_REFERENCE.md)** - For developers
- **[Troubleshooting](finance/TROUBLESHOOTING.md)** - Common issues
- **[Privacy & Security](finance/PRIVACY_SECURITY.md)** - Data protection

## Support

- **Issues**: https://github.com/ronnycoding/my-personal-agents/issues
- **Discussions**: https://github.com/ronnycoding/my-personal-agents/discussions

## Development

This feature is implemented across multiple components:

- **Issue #36**: Infrastructure & MCP command setup
- **Issue #37**: Notebook templates & helper library
- **Issue #38**: Data import & processing
- **Issue #39**: Financial analysis & metrics
- **Issue #40**: Projections & forecasting
- **Issue #41**: Visualizations & reports
- **Issue #42**: AI advisory & recommendations
- **Issue #43**: Testing suite
- **Issue #44**: Documentation

See [Epic #35](https://github.com/ronnycoding/my-personal-agents/issues/35) for full implementation details.

## License

Private - Personal Use Only

## Disclaimer

This tool provides informational financial analysis only and does not constitute professional financial advice. For personalized guidance, consult a certified financial planner.
