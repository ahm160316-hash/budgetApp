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
