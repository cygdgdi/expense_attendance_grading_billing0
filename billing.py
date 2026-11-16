# billing.py
"""Billing System module (FR-40 to FR-47)."""

from datetime import date

from validators import get_name, get_float, get_int

invoices = []

# Default tax rate and discount slabs (CRS Section 6.5) - configurable
TAX_RATE = 0.18

SLAB_1_LIMIT = 1000
SLAB_2_LIMIT = 5000
SLAB_3_LIMIT = 10000

SLAB_1_RATE = 0.05
SLAB_2_RATE = 0.10
SLAB_3_RATE = 0.15


def calculate_discount(subtotal):
    """Return the discount rate (0 to 0.15) for a subtotal."""
    if subtotal >= SLAB_3_LIMIT:
        return SLAB_3_RATE
    elif subtotal >= SLAB_2_LIMIT:
        return SLAB_2_RATE
    elif subtotal >= SLAB_1_LIMIT:
        return SLAB_1_RATE
    else:
        return 0


def calculate_tax(taxable_amount):
    """Return the tax on the amount after discount, rounded to 2 places."""
    return round(taxable_amount * TAX_RATE, 2)


def generate_invoice():
    """Create a bill: items, discount, tax, then print the invoice."""
    print("\n===== GENERATE INVOICE =====")

    customer_name = get_name("Enter customer name: ")

    items = []

    while True:
        item_name = input(
            "Enter item name (type done to stop): "
        ).strip()

        if item_name.lower() == "done":
            break

        if item_name == "":
            print("Item name cannot be empty.")
            continue

        price = get_float(
            "Enter unit price: ",
            min_val=0.01,
            error="Price must be greater than 0."
        )
        quantity = get_int(
            "Enter quantity: ",
            min_val=1,
            error="Quantity must be a whole number >= 1."
        )

        line_total = round(price * quantity, 2)

        items.append({
            "name": item_name,
            "unit_price": price,
            "quantity": quantity,
            "line_total": line_total
        })

        print("Item added successfully.")

    if not items:
        print("No items added. Invoice not generated.")
        return

    subtotal = 0

    for item in items:
        subtotal += item["line_total"]

    subtotal = round(subtotal, 2)

    discount_rate = calculate_discount(subtotal)
    discount = round(subtotal * discount_rate, 2)

    taxable_amount = round(subtotal - discount, 2)
    tax = calculate_tax(taxable_amount)

    grand_total = round(taxable_amount + tax, 2)

    bill_no = "B-" + str(len(invoices) + 1).zfill(4)
    today = date.today().strftime("%Y-%m-%d")

    invoice = {
        "bill_no": bill_no,
        "date": today,
        "customer_name": customer_name,
        "items": items,
        "subtotal": subtotal,
        "discount_rate": discount_rate,
        "discount": discount,
        "taxable_amount": taxable_amount,
        "tax": tax,
        "grand_total": grand_total
    }

    invoices.append(invoice)

    print_invoice(invoice)


def print_invoice(invoice):
    """Print one invoice in the format shown in the CRS."""
    discount_percent = round(invoice["discount_rate"] * 100)

    if invoice["discount"] > 0:
        discount_text = f"-{invoice['discount']:.2f}"
    else:
        discount_text = "0.00"

    print(f"\n{' INVOICE ':=^55}")
    print(f"Bill No  : {invoice['bill_no']}    Date: {invoice['date']}")
    print(f"Customer : {invoice['customer_name']}")

    print("-" * 55)
    print(f"{'Item':<15}{'Price':>10}{'Qty':>6}{'Total':>12}")
    print("-" * 55)

    for item in invoice["items"]:
        print(f"{item['name']:<15}"
              f"{item['unit_price']:>10.2f}"
              f"{item['quantity']:>6}"
              f"{item['line_total']:>12.2f}")

    print("-" * 55)
    print(f"{'Subtotal':<43}{invoice['subtotal']:>12.2f}")
    print(f"{'Discount (' + str(discount_percent) + '%)':<43}"
          f"{discount_text:>12}")
    print(f"{'Taxable amount':<43}{invoice['taxable_amount']:>12.2f}")
    print(f"{'Tax (' + str(round(TAX_RATE * 100)) + '%)':<43}"
          f"{invoice['tax']:>12.2f}")
    print("-" * 55)
    print(f"{'GRAND TOTAL':<43}{invoice['grand_total']:>12.2f}")
    print("=" * 55)
    print("Thank you for your purchase!")
