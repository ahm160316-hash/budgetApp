"""Core budget operations for the CSV-based CLI app."""

from typing import Any, Dict, List


def add_transaction(
    transactions: List[Dict[str, Any]],
    transaction: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Return a new transaction list with one transaction appended."""
    updated_transactions = list(transactions)
    updated_transactions.append(
        {
            "date": transaction["date"],
            "type": transaction["type"],
            "category": transaction["category"],
            "description": transaction["description"],
            "amount": transaction["amount"],
            "memo": transaction["memo"],
        }
    )
    return updated_transactions


def get_balance(transactions: List[Dict[str, Any]]) -> float:
    """Return the sum of all transaction amounts."""
    return float(sum(transaction["amount"] for transaction in transactions))


def filter_by_category(
    transactions: List[Dict[str, Any]],
    category: str,
) -> List[Dict[str, Any]]:
    """Return transactions matching the category without mutating the source."""
    normalized_category = category.casefold()
    return [
        dict(transaction)
        for transaction in transactions
        if str(transaction["category"]).casefold() == normalized_category
    ]
