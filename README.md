# Expense, Attendance, Grading & Billing Management System

A console-based, menu-driven Python application that manages **expenses, attendance, grading and billing** from one main menu. It validates everything typed in and prints clean, formatted reports.

- **Language:** Python 3.8 or newer
- **Libraries:** standard library only (no `pip install` needed)
- **Interface:** console / terminal
- **Storage:** in memory for the current session (data is lost when the program exits). Reports can optionally be exported to `.txt` files.

---

## Features

### 1. Expense Management
- Add expenses with a description, category and amount.
- Categories: **Food, Travel, Utilities, Stationery, Other** (typing is not case-sensitive).
- Amount must be a positive number with up to 2 decimal places.
- View all expenses in a table.
- Summary: category-wise totals, grand total, highest spending category, and the highest and lowest single expense.

### 2. Attendance Management
- Enter the total working days once, then add as many people as needed (name, roll number, ID, days present).
- Days present must be between 0 and the total working days.
- Attendance % = (days present ÷ total days) × 100.
- Status: **Eligible** (75% or more), **Warning** (60% to 74.99%), **Shortage** (below 60%).
- Summary: total people, average attendance, highest, lowest, and count per status.

### 3. Grading System
- Enter the number of students and the number of subjects (press Enter for the default of **5**), then each student's name, roll number and marks (separated by spaces).
- Each mark must be a number from 0 to 100 (decimals allowed).
- Calculates total, average, percentage, grade and PASS/FAIL, and prints a formatted report card.
- A student **fails if any one subject is below 35**, whatever the average.
- Class summary: total students, class average, topper, pass count and fail count.

| Percentage | Grade |
|------------|-------|
| 90 – 100   | A+    |
| 80 – 89.99 | A     |
| 70 – 79.99 | B     |
| 60 – 69.99 | C     |
| 50 – 59.99 | D     |
| 35 – 49.99 | E     |
| Below 35   | F     |

### 4. Billing System
- Enter a customer name, then add any number of items (name, unit price, quantity). Type `done` to finish.
- Bill numbers are generated automatically (`B-0001`, `B-0002`, ...) and each invoice shows today's date.
- Discount is applied by subtotal slab, then 18% tax is applied on the amount **after** discount. All money values are rounded to 2 decimals.

| Subtotal         | Discount |
|------------------|----------|
| Less than 1,000  | 0%       |
| 1,000 – 4,999.99 | 5%       |
| 5,000 – 9,999.99 | 10%      |
| 10,000 and above | 15%      |

```
line_total   = unit_price × quantity
subtotal     = sum of all line totals
discount     = subtotal × discount_rate
taxable      = subtotal − discount
tax          = taxable × 0.18
grand_total  = taxable + tax
```

### 5. Reports
- **View Reports** opens a sub-menu: Expense Report, Attendance Report, Grading Report, Billing Report, All Reports.
- Reports use aligned columns, headings, separators and 2-decimal formatting.
- If a module has no data yet, its report shows "No ... records available."
- After each report you can export it to a `.txt` file (saved in the program's folder, e.g. `expense_report.txt`).

### Input Validation

| Field          | Rule                                    | Message on bad input                     |
|----------------|-----------------------------------------|------------------------------------------|
| Menu choice    | Whole number in range                   | `Invalid choice. Enter 1-6.`             |
| Name           | Letters and spaces, 2–40 characters     | `Name must contain 2-40 letters.`        |
| Expense amount | Number greater than 0, up to 2 decimals | `Amount must be a positive number.`      |
| Category       | One of the list                         | `Choose a category from the list.`       |
| Total days     | Whole number, at least 1                | `Enter a whole number of at least 1.`    |
| Days present   | 0 to total days                         | `Days present must be between 0 and 40.` |
| Marks          | Number from 0 to 100                    | `Marks must be between 0 and 100.`       |
| Unit price     | Number greater than 0                   | `Price must be greater than 0.`          |
| Quantity       | Whole number, at least 1                | `Quantity must be a whole number >= 1.`  |

Wrong input never crashes the program or gets stored; the program shows the message and asks again. Pressing **Ctrl+C** exits cleanly with a goodbye message. On every exit the program prints how many records were entered, as a reminder that data is not saved.

---

## Project Structure

```
expense_attendance_grading_billing/
├── main.py            # entry point, main menu and sub-menus
├── validators.py      # reusable input helpers: get_int, get_float, get_name,
│                      #   get_text, get_id, get_choice, get_yes_no
├── expenses.py        # add_expense, view_expenses, expense_summary
├── attendance.py      # mark_attendance, attendance_percentage, attendance_status,
│                      #   attendance_summary, highest_lowest_attendance
├── grading.py         # calculate_grade, add_student, generate_report_card,
│                      #   view_students, class_summary
├── billing.py         # calculate_discount, calculate_tax, generate_invoice
├── reports.py         # one report per module, all reports, reports menu, export
├── tests/
│   └── test_cases.md  # 20 test cases (12 normal, 8 edge), bugs found and fixed
├── sample_output.txt  # text capture of every module running
└── README.md          # this file
```

### Settings you can change (constants at the top of each file)

| Setting                                          | File            | Default                                    |
|--------------------------------------------------|-----------------|--------------------------------------------|
| `TAX_RATE`                                       | `billing.py`    | 0.18                                       |
| `SLAB_1_LIMIT / 2 / 3` and `SLAB_1_RATE / 2 / 3` | `billing.py`    | 1000 / 5000 / 10000 and 5% / 10% / 15%     |
| `PASS_MARK`                                      | `grading.py`    | 35                                         |
| `ELIGIBLE_PERCENT`, `WARNING_PERCENT`            | `attendance.py` | 75, 60                                     |
| `CATEGORIES`                                     | `expenses.py`   | Food, Travel, Utilities, Stationery, Other |

---

## How to Run

1. Install **Python 3.8 or newer** (check with `python --version`).
2. Keep all `.py` files in the same folder.
3. Open a terminal in that folder and run:

```bash
python main.py
```

On macOS/Linux you may need `python3 main.py`.

**In PyCharm:** open the folder as a project, right-click `main.py` and choose **Run 'main'** (Shift+F10). To show Ctrl+C handling, run `python main.py` in PyCharm's Terminal tab and press Ctrl+C.

---

## Using the Program

```
==============================================
  EXPENSE | ATTENDANCE | GRADING | BILLING
==============================================
 1. Expense Management
 2. Attendance Management
 3. Grading System
 4. Billing System
 5. View Reports
 6. Exit
----------------------------------------------
Enter your choice (1-6):
```

Type a number and press Enter. Each option opens a sub-menu; choose **Back** to return. The main menu repeats until you choose **6. Exit**. A full example run is in `sample_output.txt`.

### Sample invoice

```
====================== INVOICE =======================
Bill No  : B-0001    Date: 2026-11-16
Customer : Rohan Sharma
-------------------------------------------------------
Item                Price   Qty       Total
-------------------------------------------------------
Notebook            45.00    10      450.00
Backpack           850.00     2     1700.00
Pen Box            120.00     5      600.00
-------------------------------------------------------
Subtotal                                        2750.00
Discount (5%)                                   -137.50
Taxable amount                                  2612.50
Tax (18%)                                        470.25
-------------------------------------------------------
GRAND TOTAL                                     3082.75
=======================================================
Thank you for your purchase!
```

---

## Python Concepts Used

Variables and data types (`int`, `float`, `str`, `bool`) · arithmetic, comparison and logical operators · `if / elif / else` (grades, discount slabs, attendance status) · `while True` loops for menus and re-prompting · `for` loops for marks, items and records · reusable functions with docstrings · lists (records), dictionaries (category totals, attendance records, student and invoice data) and tuples (constants) · `try / except ValueError`, `KeyboardInterrupt`, `EOFError`, `OSError` and `finally` · f-strings with alignment and precision.

---

## Testing

See **`tests/test_cases.md`** for 20 test cases covering menus, expenses, attendance, grading, billing and reports (valid, invalid, boundary, edge and robustness), the actual results, additional checks, and the list of bugs found and fixed.
