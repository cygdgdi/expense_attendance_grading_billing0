# grading.py
"""Grading System module (FR-30 to FR-36)."""

from validators import get_name, get_int

students = []

# Default pass mark (CRS Section 15) - change here if the rule changes
PASS_MARK = 35


def calculate_grade(percent):
    """Return the grade letter for a percentage using the grading scale."""
    if percent >= 90:
        return "A+"
    elif percent >= 80:
        return "A"
    elif percent >= 70:
        return "B"
    elif percent >= 60:
        return "C"
    elif percent >= 50:
        return "D"
    elif percent >= 35:
        return "E"
    else:
        return "F"


def read_marks(subjects):
    """Read one line of marks; ask again until every mark is 0 to 100."""
    while True:
        values = input(
            f"Enter {subjects} marks separated by spaces: "
        ).split()

        if len(values) != subjects:
            print("Please enter exactly", subjects, "marks.")
            continue

        try:
            # "_", "e" and "n" block 1_0, 1e1, nan and inf
            for value in values:
                if "_" in value or "e" in value.lower() \
                        or "n" in value.lower():
                    raise ValueError
            marks = [float(value) for value in values]
        except ValueError:
            print("Marks must be between 0 and 100.")
            continue

        if all(0 <= mark <= 100 for mark in marks):
            return marks

        print("Marks must be between 0 and 100.")


def add_student():
    """Enter students and marks, print report cards and a class summary."""
    print("\n===== GRADING SYSTEM =====")

    number_of_students = get_int(
        "How many students do you want to enter? ",
        min_val=1,
        error="Enter a whole number of at least 1."
    )

    subjects = get_int(
        "Enter number of subjects (default 5): ",
        min_val=1,
        default=5,
        error="Enter a whole number of at least 1."
    )

    for student_no in range(number_of_students):
        print("\nStudent", student_no + 1)

        name = get_name("Enter student name: ")

        while True:
            roll_no = input("Enter roll number: ").strip()

            if roll_no == "":
                print("Roll number cannot be empty.")
            elif any(s["roll_no"] == roll_no for s in students):
                print("Roll number already exists.")
            else:
                break

        marks = read_marks(subjects)

        total = sum(marks)
        average = total / subjects
        percentage = average

        grade = calculate_grade(percentage)

        if any(mark < PASS_MARK for mark in marks):
            result = "FAIL"
        else:
            result = "PASS"

        student = {
            "name": name,
            "roll_no": roll_no,
            "marks": marks,
            "total": total,
            "average": average,
            "percentage": percentage,
            "grade": grade,
            "result": result
        }

        students.append(student)

        generate_report_card(student)

    class_summary()


def generate_report_card(student):
    """Print a formatted report card for one student."""
    subjects = len(student["marks"])

    print(f"\n{' REPORT CARD ':=^36}")
    print("Student     :", student["name"])
    print("Roll Number :", student["roll_no"])

    print("-" * 36)
    print(f"{'Subject':<15}{'Marks':>10}")

    for i, mark in enumerate(student["marks"], start=1):
        print(f"{'Subject ' + str(i):<15}{mark:>10g}")

    print("-" * 36)
    print(f"Total       : {student['total']:g} / {subjects * 100}")
    print(f"Average     : {student['average']:.2f}")
    print(f"Percentage  : {student['percentage']:.2f}%")
    print("Grade       :", student["grade"])
    print("Result      :", student["result"])
    print("=" * 36)


def view_students():
    """Show every student in a table."""
    print("\n===== ALL STUDENTS =====")

    if not students:
        print("No student records available.")
        return

    print(f"{'Name':<18}{'Roll No':<12}"
          f"{'Percentage':<14}{'Grade':<8}{'Result'}")
    print("-" * 65)

    for student in students:
        print(f"{student['name']:<18}"
              f"{student['roll_no']:<12}"
              f"{student['percentage']:<14.2f}"
              f"{student['grade']:<8}"
              f"{student['result']}")


def class_summary():
    """Show class average, topper, pass count and fail count."""
    print("\n===== CLASS SUMMARY =====")

    if not students:
        print("No student records available.")
        return

    total_percentage = 0
    topper = students[0]
    passed = 0
    failed = 0

    for student in students:
        total_percentage += student["percentage"]

        if student["percentage"] > topper["percentage"]:
            topper = student

        if student["result"] == "PASS":
            passed += 1
        else:
            failed += 1

    class_average = total_percentage / len(students)

    print("Total students:", len(students))
    print(f"Class average: {class_average:.2f}%")
    print("Topper:", topper["name"],
          f"({topper['percentage']:.2f}%)")
    print("Pass count:", passed)
    print("Fail count:", failed)
