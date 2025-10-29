"""
Personal Finance Analysis Utility Functions

This module provides reusable functions for financial calculations, data processing,
and analysis used across all finance notebooks.

All functions are pure (no side effects) for easy testing and composition.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Union
import re


# ============================================================================
# DATA VALIDATION & CLEANING
# ============================================================================

def validate_transaction_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate transaction DataFrame against required schema.

    Args:
        df: DataFrame with transaction data

    Returns:
        Tuple of (is_valid, list of error messages)
    """
    errors = []
    required_columns = ['date', 'description', 'amount']

    # Check required columns
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
        return False, errors

    # Validate date column
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        try:
            pd.to_datetime(df['date'])
        except:
            errors.append("'date' column contains invalid dates")

    # Validate amount column
    if not pd.api.types.is_numeric_dtype(df['amount']):
        try:
            pd.to_numeric(df['amount'])
        except:
            errors.append("'amount' column contains non-numeric values")

    # Check for empty descriptions
    if df['description'].isna().any() or (df['description'] == '').any():
        errors.append("Some transactions have empty descriptions")

    # Check for zero amounts
    if (df['amount'] == 0).any():
        errors.append("Some transactions have zero amount")

    return len(errors) == 0, errors


def clean_transaction_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize transaction data.

    Args:
        df: Raw transaction DataFrame

    Returns:
        Cleaned DataFrame
    """
    df = df.copy()

    # Convert date to datetime
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Convert amount to numeric
    if not pd.api.types.is_numeric_dtype(df['amount']):
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    # Remove future dates
    df = df[df['date'] <= pd.Timestamp.now()]

    # Remove null values
    df = df.dropna(subset=['date', 'description', 'amount'])

    # Remove zero amounts
    df = df[df['amount'] != 0]

    # Strip whitespace from description
    df['description'] = df['description'].str.strip()

    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)

    return df


# ============================================================================
# TRANSACTION CATEGORIZATION
# ============================================================================

# Category mapping keywords
CATEGORY_KEYWORDS = {
    'food_dining': ['restaurant', 'cafe', 'coffee', 'pizza', 'burger', 'food', 'grocery',
                    'whole foods', 'trader joe', 'safeway', 'kroger', 'doordash', 'uber eats'],
    'transportation': ['uber', 'lyft', 'gas', 'fuel', 'parking', 'transit', 'metro',
                      'car wash', 'auto', 'vehicle', 'dmv'],
    'housing': ['rent', 'mortgage', 'utilities', 'electric', 'water', 'gas bill',
                'internet', 'cable', 'hoa', 'property tax', 'insurance'],
    'income': ['salary', 'paycheck', 'deposit', 'direct deposit', 'bonus', 'refund',
               'reimbursement', 'interest', 'dividend'],
    'shopping': ['amazon', 'target', 'walmart', 'online', 'ebay', 'etsy', 'clothing',
                 'apparel', 'shoes'],
    'healthcare': ['pharmacy', 'cvs', 'walgreens', 'doctor', 'medical', 'health',
                   'dental', 'vision', 'hospital', 'clinic'],
    'entertainment': ['netflix', 'spotify', 'hulu', 'disney', 'movie', 'theater',
                      'concert', 'game', 'subscription', 'music'],
    'travel': ['hotel', 'airbnb', 'flight', 'airline', 'vacation', 'booking', 'expedia'],
    'education': ['tuition', 'school', 'university', 'course', 'book', 'education'],
    'personal': ['haircut', 'salon', 'spa', 'gym', 'fitness', 'clothing', 'beauty'],
    'bills': ['phone', 'mobile', 'verizon', 'att', 'tmobile', 'bill payment'],
    'transfer': ['transfer', 'withdrawal', 'atm', 'cash'],
    'fees': ['fee', 'charge', 'penalty', 'late fee', 'overdraft'],
}


def categorize_transaction(description: str, amount: float = None) -> str:
    """
    Automatically categorize a transaction based on description and amount.

    Args:
        description: Transaction description
        amount: Transaction amount (positive for income, negative for expense)

    Returns:
        Category name
    """
    description_lower = description.lower()

    # Check for income based on amount (positive is income)
    if amount is not None and amount > 0:
        for keyword in CATEGORY_KEYWORDS['income']:
            if keyword in description_lower:
                return 'income'

    # Check each category's keywords
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in description_lower:
                return category

    # Default to uncategorized
    return 'uncategorized'


def categorize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add category column to transaction DataFrame.

    Args:
        df: DataFrame with 'description' and optionally 'amount' columns

    Returns:
        DataFrame with added 'category' column
    """
    df = df.copy()

    if 'amount' in df.columns:
        df['category'] = df.apply(
            lambda row: categorize_transaction(row['description'], row['amount']),
            axis=1
        )
    else:
        df['category'] = df['description'].apply(categorize_transaction)

    return df


# ============================================================================
# DUPLICATE DETECTION
# ============================================================================

def detect_duplicates(df: pd.DataFrame, existing_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Detect duplicate transactions using exact and fuzzy matching.

    Args:
        df: New transactions DataFrame
        existing_df: Existing transactions (optional)

    Returns:
        DataFrame with duplicates removed
    """
    if existing_df is None or len(existing_df) == 0:
        # No existing data, just remove exact duplicates in new data
        return df.drop_duplicates(subset=['date', 'description', 'amount'])

    # Combine for duplicate detection
    combined = pd.concat([existing_df, df], ignore_index=True)

    # Exact duplicate detection
    combined = combined.drop_duplicates(subset=['date', 'description', 'amount'], keep='first')

    # Return only new records (not in existing_df)
    new_records = combined[~combined.index.isin(existing_df.index)]

    return new_records.reset_index(drop=True)


# ============================================================================
# FINANCIAL CALCULATIONS
# ============================================================================

def calculate_net_worth(assets: Dict[str, float], liabilities: Dict[str, float]) -> float:
    """
    Calculate net worth (assets - liabilities).

    Args:
        assets: Dictionary of asset names and values
        liabilities: Dictionary of liability names and values

    Returns:
        Net worth value
    """
    total_assets = sum(assets.values())
    total_liabilities = sum(liabilities.values())
    return round(total_assets - total_liabilities, 2)


def calculate_savings_rate(income: float, expenses: float) -> float:
    """
    Calculate savings rate as percentage.

    Args:
        income: Total income
        expenses: Total expenses

    Returns:
        Savings rate (0.0 to 1.0, where 1.0 = 100%)
    """
    if income == 0:
        return 0.0

    savings = income - expenses
    rate = savings / income
    return round(rate, 4)


def calculate_emergency_fund_ratio(savings: float, monthly_expenses: float) -> float:
    """
    Calculate emergency fund adequacy (months of expenses covered).

    Args:
        savings: Current savings balance
        monthly_expenses: Average monthly expenses

    Returns:
        Number of months covered
    """
    if monthly_expenses == 0:
        return float('inf')

    return round(savings / monthly_expenses, 2)


def calculate_monthly_summary(df: pd.DataFrame, date_column: str = 'date') -> pd.DataFrame:
    """
    Aggregate transactions by month.

    Args:
        df: Transaction DataFrame
        date_column: Name of date column

    Returns:
        DataFrame with monthly aggregations
    """
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])
    df['month'] = df[date_column].dt.to_period('M')

    monthly = df.groupby('month').agg({
        'amount': ['sum', 'count', 'mean']
    }).reset_index()

    monthly.columns = ['month', 'total', 'count', 'average']
    monthly['month'] = monthly['month'].astype(str)

    return monthly


def calculate_category_summary(df: pd.DataFrame, category_column: str = 'category') -> pd.DataFrame:
    """
    Aggregate transactions by category.

    Args:
        df: Transaction DataFrame with category column
        category_column: Name of category column

    Returns:
        DataFrame with category aggregations
    """
    if category_column not in df.columns:
        raise ValueError(f"Column '{category_column}' not found in DataFrame")

    summary = df.groupby(category_column).agg({
        'amount': ['sum', 'count', 'mean']
    }).reset_index()

    summary.columns = ['category', 'total', 'count', 'average']
    summary = summary.sort_values('total', ascending=False)

    return summary


# ============================================================================
# FINANCIAL HEALTH SCORING
# ============================================================================

def calculate_financial_health_score(
    savings_rate: float,
    emergency_fund_ratio: float,
    debt_to_income: float = 0.0,
    budget_variance: float = 0.0,
    cashflow_trend: str = 'neutral'
) -> int:
    """
    Calculate overall financial health score (0-100).

    Factors:
    - Savings rate (30%): >20% excellent, 10-20% good, <10% poor
    - Emergency fund (25%): ≥6mo excellent, 3-6mo good, <3mo poor
    - Debt-to-income (20%): <20% excellent, 20-35% good, >35% poor
    - Budget adherence (15%): <5% variance excellent, 5-15% good, >15% poor
    - Cash flow trend (10%): positive excellent, neutral good, negative poor

    Args:
        savings_rate: Savings rate (0.0 to 1.0)
        emergency_fund_ratio: Months of expenses covered
        debt_to_income: Debt-to-income ratio (0.0 to 1.0)
        budget_variance: Budget variance percentage (0.0 to 1.0)
        cashflow_trend: 'positive', 'neutral', or 'negative'

    Returns:
        Financial health score (0-100)
    """
    score = 0

    # Savings rate (0-30 points)
    if savings_rate >= 0.20:
        score += 30
    elif savings_rate >= 0.10:
        score += 20
    elif savings_rate >= 0.05:
        score += 10
    else:
        score += int(savings_rate * 100)

    # Emergency fund (0-25 points)
    if emergency_fund_ratio >= 6.0:
        score += 25
    elif emergency_fund_ratio >= 3.0:
        score += 15
    elif emergency_fund_ratio >= 1.0:
        score += 8
    else:
        score += int(emergency_fund_ratio * 8)

    # Debt-to-income (0-20 points)
    if debt_to_income < 0.20:
        score += 20
    elif debt_to_income < 0.35:
        score += 12
    else:
        score += max(0, int(20 - debt_to_income * 40))

    # Budget adherence (0-15 points)
    if budget_variance < 0.05:
        score += 15
    elif budget_variance < 0.15:
        score += 10
    else:
        score += max(0, int(15 - budget_variance * 60))

    # Cash flow trend (0-10 points)
    if cashflow_trend == 'positive':
        score += 10
    elif cashflow_trend == 'neutral':
        score += 5
    else:
        score += 0

    return min(score, 100)


# ============================================================================
# FORECASTING & PROJECTIONS
# ============================================================================

SCENARIO_PARAMETERS = {
    'conservative': {
        'income_growth': 0.02,  # 2% annual
        'expense_growth': 0.03,  # 3% annual
        'investment_return': 0.05,  # 5% annual
    },
    'moderate': {
        'income_growth': 0.04,  # 4% annual
        'expense_growth': 0.03,  # 3% annual
        'investment_return': 0.07,  # 7% annual
    },
    'aggressive': {
        'income_growth': 0.06,  # 6% annual
        'expense_growth': 0.02,  # 2% annual
        'investment_return': 0.10,  # 10% annual
    },
}


def project_cashflow(
    avg_monthly_income: float,
    avg_monthly_expenses: float,
    months: int = 12,
    scenario: str = 'moderate'
) -> pd.DataFrame:
    """
    Project future cash flow based on historical averages and scenario.

    Args:
        avg_monthly_income: Average monthly income
        avg_monthly_expenses: Average monthly expenses
        months: Number of months to project
        scenario: 'conservative', 'moderate', or 'aggressive'

    Returns:
        DataFrame with projected monthly cash flow
    """
    params = SCENARIO_PARAMETERS.get(scenario, SCENARIO_PARAMETERS['moderate'])

    monthly_income_growth = params['income_growth'] / 12
    monthly_expense_growth = params['expense_growth'] / 12

    projections = []
    for month in range(1, months + 1):
        projected_income = avg_monthly_income * (1 + monthly_income_growth) ** month
        projected_expenses = avg_monthly_expenses * (1 + monthly_expense_growth) ** month
        projected_cashflow = projected_income - projected_expenses

        projections.append({
            'month': month,
            'income': round(projected_income, 2),
            'expenses': round(projected_expenses, 2),
            'cashflow': round(projected_cashflow, 2),
            'scenario': scenario
        })

    return pd.DataFrame(projections)


def calculate_savings_goal_progress(
    current_savings: float,
    goal_amount: float,
    months_remaining: int,
    monthly_contribution: float,
    annual_return: float = 0.05
) -> Dict[str, Union[float, bool]]:
    """
    Calculate progress toward savings goal with compound growth.

    Args:
        current_savings: Current savings balance
        goal_amount: Target savings amount
        months_remaining: Months until goal date
        monthly_contribution: Expected monthly contribution
        annual_return: Expected annual return rate

    Returns:
        Dictionary with projection results
    """
    monthly_return = annual_return / 12

    # Future value of current savings
    fv_current = current_savings * (1 + monthly_return) ** months_remaining

    # Future value of monthly contributions (annuity)
    if monthly_return == 0:
        fv_contributions = monthly_contribution * months_remaining
    else:
        fv_contributions = monthly_contribution * (
            ((1 + monthly_return) ** months_remaining - 1) / monthly_return
        )

    projected_total = fv_current + fv_contributions

    return {
        'projected_balance': round(projected_total, 2),
        'goal_amount': round(goal_amount, 2),
        'on_track': projected_total >= goal_amount,
        'shortfall': round(max(0, goal_amount - projected_total), 2),
        'surplus': round(max(0, projected_total - goal_amount), 2),
        'progress_percentage': round((projected_total / goal_amount) * 100, 1) if goal_amount > 0 else 0
    }


def calculate_debt_payoff(
    principal: float,
    annual_interest_rate: float,
    monthly_payment: float
) -> Dict[str, Union[float, int]]:
    """
    Calculate debt payoff timeline and total interest.

    Args:
        principal: Initial loan amount
        annual_interest_rate: Annual interest rate (e.g., 0.05 for 5%)
        monthly_payment: Monthly payment amount

    Returns:
        Dictionary with payoff details
    """
    monthly_rate = annual_interest_rate / 12

    if monthly_payment <= principal * monthly_rate:
        return {
            'error': 'Monthly payment too low - will never pay off debt',
            'minimum_payment': round(principal * monthly_rate * 1.1, 2)
        }

    months = 0
    total_interest = 0
    remaining = principal

    while remaining > 0 and months < 600:  # Cap at 50 years
        interest_charge = remaining * monthly_rate
        principal_payment = min(monthly_payment - interest_charge, remaining)

        total_interest += interest_charge
        remaining -= principal_payment
        months += 1

    return {
        'months_to_payoff': months,
        'years_to_payoff': round(months / 12, 1),
        'total_interest_paid': round(total_interest, 2),
        'total_amount_paid': round(principal + total_interest, 2),
    }


# ============================================================================
# DATA FORMATTING
# ============================================================================

def format_currency(amount: float, currency: str = 'USD') -> str:
    """
    Format amount as currency string.

    Args:
        amount: Numeric amount
        currency: Currency code

    Returns:
        Formatted currency string
    """
    if currency == 'USD':
        return f"${amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"


def format_percentage(value: float) -> str:
    """
    Format value as percentage string.

    Args:
        value: Decimal value (e.g., 0.25 for 25%)

    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.1f}%"
