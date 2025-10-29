# Finance Notebooks Storage

This directory stores your personal finance analysis Jupyter notebooks created by the `/finance` command.

## 🔒 Privacy & Security

**IMPORTANT**: All files in this directory contain sensitive financial data and are excluded from git tracking.

- All `.ipynb` notebook files are gitignored
- Transaction data files (CSV, Excel, JSON) are gitignored
- Generated reports are gitignored
- Only infrastructure files are tracked (README.md, .gitignore, finance_utils.py)

## 📁 Directory Structure

```
finance-notebooks/
├── .gitignore              # Git exclusion rules
├── README.md               # This file
├── finance_utils.py        # Helper functions library
├── reports/                # Generated reports (PNG, PDF)
└── *.ipynb                 # Your financial notebooks (gitignored)
```

## 📊 Notebook Naming Convention

Notebooks are automatically named with timestamps for easy sorting:

- `2025-01-budget.ipynb` - Monthly budget notebook
- `2025-Q1-analysis.ipynb` - Quarterly analysis
- `personal-finance-2025.ipynb` - Annual overview

## 🛠️ Helper Library

The `finance_utils.py` file contains reusable Python functions for:

- Financial calculations (net worth, savings rate, etc.)
- Transaction categorization
- Data validation and cleaning
- Common data transformations

## 🔐 Data Backup

Since notebooks are gitignored, remember to:

1. **Backup regularly** to a secure location
2. **Encrypt backups** if storing in cloud services
3. **Use strong passwords** for encrypted archives
4. **Test restore process** periodically

## 📝 Usage

Notebooks are created and managed through the `/finance` command:

```bash
# Create new notebook
/finance init --notebook="2025-budget"

# List existing notebooks
/finance list

# Delete notebook
/finance delete --notebook="2025-budget"
```

## ⚠️ Warning

Never commit financial data to version control. This directory's .gitignore ensures your sensitive data stays local.
