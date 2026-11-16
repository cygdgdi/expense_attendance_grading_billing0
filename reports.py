# reports.py
"""Reports module (FR-50 to FR-53)."""

import contextlib
import io

from validators import get_int, get_yes_no


# 1. Expense Report
def print_expense_report(expenses):
    """Print all expenses with a grand total and category-wise totals."""
    print("\n========== EXPENSE REPORT ==========")

    if not expenses:
        print("No expense records available.")
        return

    total = 0
    category_totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        total += amount

        category_totals[category] = (
            category_totals.get(category, 0) + amount
        )

    print(f"{'Description':<18}{'Category':<15}{'Amount':>10}")
    print("-" * 43)

    for expense in expenses:
        print(f"{expense['description']:<18}"
              f"{expense['category']:<15}"
              f"{expense['amount']:>10.2f}")

    print("-" * 43)
    print(f"Grand Total: {total:.2f}")

    print("\nCategory-wise Total:")

    for category, amount in category_totals.items():
        print(f"{category:<18}{amount:>10.2f}")


# 2. Attendance Report
def print_attendance_report(attendance):
    """Print attendance records with average, highest and lowest."""
    print("\n========== ATTENDANCE REPORT ==========")

    if not attendance:
        print("No attendance records available.")
        return

    total_percentage = 0

    highest = None
    lowest = None

    print(f"{'Name':<15}{'Roll No':<12}{'Percentage':<14}{'Status'}")
    print("-" * 55)

    for roll_no, record in attendance.items():
        percentage = record["percentage"]

        total_percentage += percentage

        if highest is None:
            highest = record
            lowest = record
        else:
            if percentage > highest["percentage"]:
                highest = record

            if percentage < lowest["percentage"]:
                lowest = record

        print(f"{record['name']:<15}"
              f"{roll_no:<12}"
              f"{percentage:<14.2f}"
              f"{record['status']}")

    average = total_percentage / len(attendance)

    print("\nTotal people:", len(attendance))
    print(f"Average attendance: {average:.2f}%")
    print("Highest attendance:", highest["name"],
          f"({highest['percentage']:.2f}%)")
    print("Lowest attendance:", lowest["name"],
          f"({lowest['percentage']:.2f}%)")


# 3. Grading Report
def print_grading_report(students):
    """Print all students with class average, topper, pass/fail counts."""
    print("\n========== GRADING REPORT ==========")

    if not students:
        print("No student records available.")
        return

    total_percentage = 0

    passed = 0
    failed = 0

    topper = students[0]

    print(f"{'Name':<18}{'Roll No':<12}{'Percentage':<14}"
          f"{'Grade':<8}{'Result'}")
    print("-" * 65)

    for student in students:
        percentage = student["percentage"]

        total_percentage += percentage

        if percentage > topper["percentage"]:
            topper = student

        if student["result"] == "PASS":
            passed += 1
        else:
            failed += 1

        print(f"{student['name']:<18}"
              f"{student['roll_no']:<12}"
              f"{percentage:<14.2f}"
              f"{student['grade']:<8}"
              f"{student['result']}")

    average = total_percentage / len(students)

    print("\nTotal students:", len(students))
    print(f"Class average: {average:.2f}%")
    print("Topper:", topper["name"], f"({topper['percentage']:.2f}%)")
    print("Pass count:", passed)
    print("Fail count:", failed)


# 4. Billing Report
def print_invoice_report(invoices):
    """Print every invoice and the total sales."""
    print("\n========== BILLING REPORT ==========")

    if not invoices:
        print("No invoice records available.")
        return

    total_sales = 0

    for invoice in invoices:
        print("\nBill No:", invoice["bill_no"], "  Date:", invoice["date"])
        print("Customer:", invoice["customer_name"])
        print("-" * 45)
        print(f"{'Item':<18}{'Qty':>6}{'Total':>12}")
        print("-" * 45)

        for item in invoice["items"]:
            print(f"{item['name']:<18}"
                  f"{item['quantity']:>6}"
                  f"{item['line_total']:>12.2f}")

        print("-" * 45)
        print(f"Subtotal: {invoice['subtotal']:.2f}")
        print(f"Discount: {invoice['discount']:.2f}")
        print(f"Tax: {invoice['tax']:.2f}")
        print(f"Grand Total: {invoice['grand_total']:.2f}")

        total_sales += invoice["grand_total"]

    print("\nTotal invoices:", len(invoices))
    print(f"Total sales: {total_sales:.2f}")


# 5. All reports together
def reports(expenses, attendance, students, invoices):
    """Print the four reports one after another."""
    print("\n======================================")
    print("          ALL SYSTEM REPORTS")
    print("======================================")

    print_expense_report(expenses)
    print_attendance_report(attendance)
    print_grading_report(students)
    print_invoice_report(invoices)

    print("\n======================================")
    print("       ALL REPORTS COMPLETED")
    print("======================================")


def show_report(report_function, data, filename):
    """Print a report, then offer to export it to a .txt file (FR-53)."""
    buffer = io.StringIO()

    with contextlib.redirect_stdout(buffer):
        report_function(*data)

    text = buffer.getvalue()
    print(text, end="")

    if get_yes_no("\nExport this report to a .txt file? (yes/no): "):
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(text)
            print("Report saved to", filename)
        except OSError:
            print("Could not save the report file.")


def reports_menu(expenses, attendance, students, invoices):
    """Reports sub-menu: one report per module, or all of them."""
    while True:
        print("\n--- REPORTS ---")
        print(" 1. Expense Report")
        print(" 2. Attendance Report")
        print(" 3. Grading Report")
        print(" 4. Billing Report")
        print(" 5. All Reports")
        print(" 6. Back")

        choice = get_int("Enter your choice (1-6): ", 1, 6,
                         error="Invalid choice. Enter 1-6.")

        if choice == 1:
            show_report(print_expense_report, (expenses,),
                        "expense_report.txt")
        elif choice == 2:
            show_report(print_attendance_report, (attendance,),
                        "attendance_report.txt")
        elif choice == 3:
            show_report(print_grading_report, (students,),
                        "grading_report.txt")
        elif choice == 4:
            show_report(print_invoice_report, (invoices,),
                        "billing_report.txt")
        elif choice == 5:
            show_report(reports, (expenses, attendance, students, invoices),
                        "all_reports.txt")
        elif choice == 6:
            break
