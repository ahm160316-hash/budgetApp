"""Tests for budget core operations."""

import csv
from pathlib import Path
from typing import Any, Dict, List

from budget.core import (
    add_transaction,
    filter_by_category,
    get_balance,
    load_transactions_from_csv,
)


def load_step2_transactions() -> List[Dict[str, Any]]:
    csv_path = Path(__file__).parent.parent / "data" / "step2_transactions.csv"
    with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
        return [
            {
                "date": row["date"],
                "type": row["type"],
                "category": row["category"],
                "description": row["description"],
                "amount": int(row["amount"]),
                "memo": row["memo"],
            }
            for row in csv.DictReader(csv_file)
        ]


def test_add_transaction_increases_length() -> None:
    transactions = []
    transaction = {
        "date": "2026-01-01",
        "type": "income",
        "category": "salary",
        "description": "January salary",
        "amount": 3000000,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1


def test_get_balance_returns_zero_for_empty_transactions() -> None:
    assert get_balance([]) == 0.0


def test_get_balance_sums_income_and_expense_amounts() -> None:
    transactions = [
        {
            "date": "2026-01-01",
            "type": "income",
            "category": "salary",
            "description": "January salary",
            "amount": 3000000,
            "memo": "",
        },
        {
            "date": "2026-01-02",
            "type": "expense",
            "category": "food",
            "description": "Lunch",
            "amount": -12000,
            "memo": "",
        },
    ]

    assert get_balance(transactions) == 2988000.0


def test_get_balance_with_step2_transactions_csv() -> None:
    transactions = load_step2_transactions()

    assert get_balance(transactions) == 24285027.0


def test_filter_by_category_matches_step2_transactions_csv() -> None:
    transactions = load_step2_transactions()

    result = filter_by_category(transactions, "급여")

    assert len(result) == 9
    assert all(transaction["category"] == "급여" for transaction in result)


def test_filter_by_category_returns_empty_list_for_missing_category() -> None:
    transactions = load_step2_transactions()

    assert filter_by_category(transactions, "없는카테고리") == []


def test_filter_by_category_returns_independent_results() -> None:
    transactions = load_step2_transactions()
    original_salary = next(
        transaction
        for transaction in transactions
        if transaction["category"] == "급여"
    )
    original_memo = original_salary["memo"]

    result = filter_by_category(transactions, "급여")
    result[0]["memo"] = "changed"

    assert original_salary["memo"] == original_memo


def test_load_transactions_from_csv_reads_step1_transactions() -> None:
    csv_path = Path(__file__).parent.parent / "data" / "step1_transactions.csv"

    transactions = load_transactions_from_csv(csv_path)

    assert len(transactions) == 10
    assert transactions[0] == {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }
    assert isinstance(transactions[0]["amount"], int)
