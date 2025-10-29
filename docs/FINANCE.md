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

| Command | Description |
|---------|-------------|
| `/finance init` | Create new financial notebook |
| `/finance import` | Import transaction data from CSV/Excel |
| `/finance analyze` | Analyze financial data and calculate metrics |
| `/finance project` | Generate projections and forecasts |
| `/finance advise` | Get AI-driven recommendations |
| `/finance report` | Create charts and visualizations |
| `/finance list` | List all notebooks |
| `/finance delete` | Delete a notebook |

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

## Data Sources

Import transactions from:
- Bank account downloads (CSV/Excel)
- Credit card statements
- Manual entry via notebook

Supported formats:
- CSV with date, description, amount columns
- Excel (.xlsx, .xls)
- Multiple date formats supported

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
