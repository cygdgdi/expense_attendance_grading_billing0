# expenses.py
"""Expense Management module (FR-10 to FR-15)."""

from validators import get_text, get_float, get_choice, get_yes_no

expenses = []

CATEGORIES = ("Food", "Travel", "Utilities", "Stationery", "Other")


def add_expense():
    """Add one or more expenses: description, category and amount."""
    print("\n===== ADD EXPENSE =====")

    while True:
        description = get_text("Description: ")

        category = get_choice(
            "Category (" + "/".join(CATEGORIES) + "): ",
            CATEGORIES,
            "Choose a category from the list."
        )

        amount = get_float(
            "Amount: ",
            min_val=0.01,
            error="Amount must be a positive number."
        )

        expenses.append({
            "description": description,
            "category": category,
            "amount": amount
        })

        print("Expense added successfully!")

        if not get_yes_no("Add another expense? (yes/no): "):
            break


def view_expenses():
    """Show every recorded expense in a table."""
    print("\n===== ALL EXPENSES =====")

    if not expenses:
        print("No expense records available.")
        return

    print(f"{'Description':<20}{'Category':<15}{'Amount':>12}")
    print("-" * 47)

    for expense in expenses:
        print(f"{expense['description']:<20}"
              f"{expense['category']:<15}"
              f"{expense['amount']:>12.2f}")


def expense_summary():
    """Show category totals, grand total, highest and lowest expense."""
    print("\n===== EXPENSE SUMMARY =====")

    if not expenses:
        print("No expense records available.")
        return

    category_totals = {}

    total = 0
    highest = expenses[0]
    lowest = expenses[0]

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        category_totals[category] = (
            category_totals.get(category, 0) + amount
        )

        total += amount

        if amount > highest["amount"]:
            highest = expense

        if amount < lowest["amount"]:
            lowest = expense

    print(f"{'CATEGORY':<20}{'TOTAL':>12}")
    print("-" * 32)

    for category, amount in category_totals.items():
        print(f"{category:<20}{amount:>12.2f}")

    print("-" * 32)
    print(f"{'GRAND TOTAL':<20}{total:>12.2f}")

    top_category = max(category_totals, key=category_totals.get)

    print("\nHighest spending category:",
          top_category, f"({category_totals[top_category]:.2f})")

    print("Highest single expense:",
          highest["description"], f"({highest['amount']:.2f})")

    print("Lowest single expense:",
          lowest["description"], f"({lowest['amount']:.2f})")
