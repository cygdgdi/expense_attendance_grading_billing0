# attendance.py
"""Attendance Management module (FR-20 to FR-25)."""

from validators import get_name, get_id, get_int, get_yes_no

attendance_records = {}

# Default thresholds (CRS Section 15) - change here if the rules change
ELIGIBLE_PERCENT = 75
WARNING_PERCENT = 60


def attendance_percentage(present_days, total_days):
    """Return attendance % = (days present / total days) x 100."""
    if total_days == 0:  # avoid ZeroDivisionError
        return 0
    return (present_days / total_days) * 100


def attendance_status(percent):
    """Return Eligible, Warning or Shortage for an attendance %."""
    if percent >= ELIGIBLE_PERCENT:
        return "Eligible"
    elif percent >= WARNING_PERCENT:
        return "Warning"
    else:
        return "Shortage"


def mark_attendance():
    """Enter total working days, then add people with days present."""
    print("\n===== MARK ATTENDANCE =====")

    total_days = get_int(
        "Enter total working days: ",
        min_val=1,
        error="Enter a whole number of at least 1."
    )

    while True:
        name = get_name("Enter name: ")

        while True:
            roll_no = input("Enter roll number: ").strip()

            if roll_no == "":
                print("Roll number cannot be empty.")
            elif roll_no in attendance_records:
                print("Roll number already exists. Enter another.")
            else:
                break

        student_id = get_id("Enter ID: ")

        present_days = get_int(
            "Enter days present: ",
            min_val=0,
            max_val=total_days,
            error=f"Days present must be between 0 and {total_days}."
        )

        percentage = attendance_percentage(present_days, total_days)
        status = attendance_status(percentage)

        attendance_records[roll_no] = {
            "name": name,
            "roll_no": roll_no,
            "id": student_id,
            "total_days": total_days,
            "present_days": present_days,
            "percentage": percentage,
            "status": status
        }

        print("Attendance saved successfully!")
        print(f"Attendance: {percentage:.2f}%")
        print("Status:", status)

        if not get_yes_no("Add another person? (yes/no): "):
            break


def attendance_summary():
    """Show the attendance table, average, highest, lowest, status counts."""
    print("\n===== ATTENDANCE SUMMARY =====")

    if not attendance_records:
        print("No attendance records available.")
        return

    total_percentage = 0
    highest = None
    lowest = None

    eligible = 0
    warning = 0
    shortage = 0

    print(f"{'Name':<15}{'Roll No':<10}{'Total Days':<12}"
          f"{'Present':<10}{'Attendance %':<15}{'Status'}")
    print("-" * 72)

    for roll_no, record in attendance_records.items():
        percent = record["percentage"]
        total_percentage += percent

        print(f"{record['name']:<15}"
              f"{roll_no:<10}"
              f"{record['total_days']:<12}"
              f"{record['present_days']:<10}"
              f"{percent:<15.2f}"
              f"{record['status']}")

        if highest is None:
            highest = record
            lowest = record
        else:
            if percent > highest["percentage"]:
                highest = record

            if percent < lowest["percentage"]:
                lowest = record

        if record["status"] == "Eligible":
            eligible += 1
        elif record["status"] == "Warning":
            warning += 1
        else:
            shortage += 1

    count = len(attendance_records)
    average = total_percentage / count

    print("\nSummary:")
    print(f"Total people       : {count}")
    print(f"Average attendance : {average:.2f}%")
    print(f"Highest            : {highest['name']} "
          f"({highest['percentage']:.2f}%)")
    print(f"Lowest             : {lowest['name']} "
          f"({lowest['percentage']:.2f}%)")
    print(f"Eligible: {eligible} | Warning: {warning} | "
          f"Shortage: {shortage}")


def highest_lowest_attendance():
    """Show only the highest and lowest attendance."""
    print("\n===== HIGHEST AND LOWEST ATTENDANCE =====")

    if not attendance_records:
        print("No attendance records available.")
        return

    highest = None
    lowest = None

    for record in attendance_records.values():
        if highest is None:
            highest = record
            lowest = record
        else:
            if record["percentage"] > highest["percentage"]:
                highest = record

            if record["percentage"] < lowest["percentage"]:
                lowest = record

    print("Highest attendance:",
          highest["name"], f"({highest['percentage']:.2f}%)")

    print("Lowest attendance:",
          lowest["name"], f"({lowest['percentage']:.2f}%)")
