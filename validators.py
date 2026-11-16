# validators.py
"""Reusable input-validation helpers (CRS Section 7).

Every helper keeps asking until the user types something valid, so wrong
input can never crash the program or be stored.
"""


def get_int(prompt, min_val=None, max_val=None, error=None, default=None):
    """Ask for a whole number and re-prompt until it is valid and in range.

    error   -- message shown for ANY invalid entry (optional)
    default -- value returned when the user just presses Enter (optional)
    """
    while True:
        value = input(prompt).strip()

        if value == "" and default is not None:
            return default

        try:
            if "_" in value:  # Python would accept int("1_0"), so block it
                raise ValueError
            number = int(value)
        except ValueError:
            print(error or "Please enter a valid whole number.")
            continue

        if min_val is not None and number < min_val:
            print(error or f"Value must be at least {min_val}.")
        elif max_val is not None and number > max_val:
            print(error or f"Value must not exceed {max_val}.")
        else:
            return number


def get_float(prompt, min_val=None, max_val=None, decimal_places=2,
              error=None):
    """Ask for a decimal number and re-prompt until it is valid and in range.

    Allows up to `decimal_places` digits after the decimal point.
    """
    while True:
        value = input(prompt).strip().lower()

        try:
            # "_", "e" and "n" block 1_0, 1e3, nan and inf
            if "_" in value or "e" in value or "n" in value:
                raise ValueError
            number = float(value)
        except ValueError:
            print(error or "Invalid input. Please enter a number.")
            continue

        if "." in value and len(value.split(".")[1]) > decimal_places:
            print(f"Use at most {decimal_places} decimal places.")
        elif min_val is not None and number < min_val:
            print(error or f"Value must be at least {min_val}.")
        elif max_val is not None and number > max_val:
            print(error or f"Value must not exceed {max_val}.")
        else:
            return number


def get_name(prompt):
    """Ask for a person's name: letters and spaces only, 2-40 characters."""
    while True:
        name = input(prompt).strip()

        if 2 <= len(name) <= 40 and name.replace(" ", "").isalpha():
            return name

        print("Name must contain 2-40 letters.")


def get_text(prompt, field="Description", max_len=50):
    """Ask for free text (e.g. an expense description) that is not empty."""
    while True:
        text = input(prompt).strip()

        if text == "":
            print(f"{field} cannot be empty.")
        elif len(text) > max_len:
            print(f"{field} must be at most {max_len} characters.")
        else:
            return text


def get_id(prompt):
    """Ask for an ID made only of letters and digits (e.g. A101 or 101)."""
    while True:
        value = input(prompt).strip()

        if value.isalnum():
            return value

        print("ID must contain only letters and digits.")


def get_choice(prompt, options, error="Choose an option from the list."):
    """Ask for one value from `options` (not case-sensitive)."""
    while True:
        value = input(prompt).strip().lower()

        for option in options:
            if option.lower() == value:
                return option

        print(error)


def get_yes_no(prompt):
    """Ask a yes/no question and return True for yes, False for no."""
    while True:
        choice = input(prompt).strip().lower()

        if choice in ("yes", "y"):
            return True
        elif choice in ("no", "n"):
            return False
        else:
            print("Please enter yes or no.")
