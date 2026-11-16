# main.py
"""Entry point and menus for the Expense, Attendance, Grading and
Billing Management System.  Run with:  python main.py
"""

from expenses import (
    add_expense, view_expenses, expense_summary, expenses
)
from attendance import (
    mark_attendance, attendance_summary, highest_lowest_attendance,
    attendance_records
)
from grading import add_student, view_students, class_summary, students
from billing import generate_invoice, invoices
from reports import reports_menu
from validators import get_int


def ask_choice(high):
    """Read a menu choice from 1 to `high` (CRS error message on bad input)."""
    return get_int(
        f"Enter your choice (1-{high}): ", 1, high,
        error=f"Invalid choice. Enter 1-{high}."
    )


def print_menu(title, options):
    """Print a sub-menu with numbered options."""
    print(f"\n--- {title} ---")

    for number, text in enumerate(options, start=1):
        print(f" {number}. {text}")


def display_menu():
    """Print the main menu."""
    print("\n" + "=" * 46)
    print("  EXPENSE | ATTENDANCE | GRADING | BILLING")
    print("=" * 46)
    print(" 1. Expense Management")
    print(" 2. Attendance Management")
    print(" 3. Grading System")
    print(" 4. Billing System")
    print(" 5. View Reports")
    print(" 6. Exit")
    print("-" * 46)


def expense_menu():
    """Expense Management sub-menu."""
    while True:
        print_menu("EXPENSE MANAGEMENT", [
            "Add Expense", "View All Expenses", "Expense Summary", "Back"
        ])

        choice = ask_choice(4)

        if choice == 1:
            add_expense()
        elif choice == 2:
            view_expenses()
        elif choice == 3:
            expense_summary()
        elif choice == 4:
            break


def attendance_menu():
    """Attendance Management sub-menu."""
    while True:
        print_menu("ATTENDANCE MANAGEMENT", [
            "Mark Attendance", "Attendance Summary",
            "Highest and Lowest Attendance", "Back"
        ])

        choice = ask_choice(4)

        if choice == 1:
            mark_attendance()
        elif choice == 2:
            attendance_summary()
        elif choice == 3:
            highest_lowest_attendance()
        elif choice == 4:
            break


def grading_menu():
    """Grading System sub-menu."""
    while True:
        print_menu("GRADING SYSTEM", [
            "Add Students and Marks", "View All Students",
            "Class Summary", "Back"
        ])

        choice = ask_choice(4)

        if choice == 1:
            add_student()
        elif choice == 2:
            view_students()
        elif choice == 3:
            class_summary()
        elif choice == 4:
            break


def billing_menu():
    """Billing System sub-menu."""
    while True:
        print_menu("BILLING SYSTEM", ["Generate Invoice", "Back"])

        choice = ask_choice(2)

        if choice == 1:
            generate_invoice()
        elif choice == 2:
            break


def main():
    """Show the main menu in a loop until the user chooses Exit."""
    while True:
        display_menu()

        choice = ask_choice(6)

        if choice == 1:
            expense_menu()
        elif choice == 2:
            attendance_menu()
        elif choice == 3:
            grading_menu()
        elif choice == 4:
            billing_menu()
        elif choice == 5:
            reports_menu(expenses, attendance_records, students, invoices)
        elif choice == 6:
            print("\nThank you for using the system. Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C (or closed input) ends the program cleanly
        print("\n\nProgram interrupted. Goodbye!")
    finally:
        # Runs on every exit (normal exit or Ctrl+C)
        total = (len(expenses) + len(attendance_records)
                 + len(students) + len(invoices))
        print(f"Session ended. {total} record(s) entered "
              "(data is not saved after exit).")
