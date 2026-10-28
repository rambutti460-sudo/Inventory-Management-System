
import json
import os

FILE_NAME = "inventory.json"


# Load inventory from a JSON file
def load_inventory():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)

            if isinstance(data, dict):
                return data

            print("Warning: Invalid inventory file format.")
            return {}

        except (json.JSONDecodeError, OSError):
            print("Warning: Unable to read inventory file.")
            return {}

    return {}


# Save inventory to a JSON file
def save_inventory(inventory):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(inventory, file, indent=4)
        return True
    except OSError:
        print("Error: Unable to save inventory.")
        return False


# Read a non-empty string
def read_text(message):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input cannot be empty.")


# Read a valid number
def read_number(message, minimum=0, allow_zero=True):
    while True:
        try:
            value = float(input(message))

            if value < minimum:
                print(f"Value must be at least {minimum}.")
            elif not allow_zero and value == 0:
                print("Value must be greater than zero.")
            else:
                return value

        except ValueError:
            print("Please enter a valid number.")


# Read a whole number
def read_integer(message, minimum=0):
    while True:
        try:
            value = int(input(message))

            if value < minimum:
                print(f"Value must be at least {minimum}.")
            else:
                return value

        except ValueError:
            print("Please enter a valid whole number.")


# Add a product
def add_product(inventory):
    print("\n--- Add Product ---")

    product_id = read_text("Enter Product ID: ")

    if product_id in inventory:
        print("Product ID already exists.")
        return

    name = read_text("Enter Product Name: ")
    category = read_text("Enter Category: ")
    price = read_number("Enter Unit Price (Rs.): ", 0, False)
    quantity = read_integer("Enter Initial Quantity: ")
    min_stock = read_integer("Enter Low-Stock Threshold: ", 1)

    product = {
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity,
        "min_stock": min_stock
    }

    inventory[product_id] = product

    if save_inventory(inventory):
        print("Product added successfully!")
    else:
        inventory.pop(product_id)


# Display one product
def display_product(product_id, product):
    print("\nProduct ID:", product_id)
    print("Name:", product["name"])
    print("Category:", product["category"])
    print("Unit Price: Rs.", f'{product["price"]:.2f}')
    print("Quantity:", product["quantity"])
    print("Stock Value: Rs.",
          f'{product["price"] * product["quantity"]:.2f}')
    print("Low-Stock Threshold:", product["min_stock"])

    if product["quantity"] <= product["min_stock"]:
        print("Stock Status: LOW STOCK")
    else:
        print("Stock Status: Available")

    print("-" * 40)


# View all products
def view_products(inventory):
    print("\n--- Inventory List ---")

    if not inventory:
        print("No products available.")
        return

    for product_id, product in inventory.items():
        display_product(product_id, product)


# Search for a product
def search_product(inventory):
    print("\n--- Search Product ---")
    product_id = read_text("Enter Product ID: ")

    if product_id in inventory:
        display_product(product_id, inventory[product_id])
    else:
        print("Product not found.")


# Update product price or quantity
def update_product(inventory):
    print("\n--- Update Product ---")
    product_id = read_text("Enter Product ID: ")

    if product_id not in inventory:
        print("Product not found.")
        return

    product = inventory[product_id]
    display_product(product_id, product)

    print("1. Update Price")
    print("2. Update Quantity")
    print("3. Update Low-Stock Threshold")

    choice = input("Choose an option (1-3): ").strip()

    if choice == "1":
        product["price"] = read_number(
            "Enter New Price (Rs.): ", 0, False
        )

    elif choice == "2":
        product["quantity"] = read_integer(
            "Enter New Quantity: "
        )

    elif choice == "3":
        product["min_stock"] = read_integer(
            "Enter New Threshold: ", 1
        )

    else:
        print("Invalid choice.")
        return

    if save_inventory(inventory):
        print("Product updated successfully!")


# Delete a product
def delete_product(inventory):
    print("\n--- Delete Product ---")
    product_id = read_text("Enter Product ID: ")

    if product_id not in inventory:
        print("Product not found.")
        return

    product = inventory[product_id]
    confirm = input(
        f"Delete {product['name']}? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        deleted_product = inventory.pop(product_id)

        if save_inventory(inventory):
            print("Product deleted successfully!")
        else:
            inventory[product_id] = deleted_product
    else:
        print("Deletion cancelled.")


# Sell products and reduce stock
def sell_product(inventory):
    print("\n--- Sell Product ---")
    product_id = read_text("Enter Product ID: ")

    if product_id not in inventory:
        print("Product not found.")
        return

    product = inventory[product_id]
    display_product(product_id, product)

    quantity = read_integer("Enter Quantity to Sell: ", 1)

    if quantity > product["quantity"]:
        print("Insufficient stock! Sale cancelled.")
        return

    old_quantity = product["quantity"]
    old_quantity_sold = quantity
    total = product["price"] * quantity

    product["quantity"] -= quantity

    if save_inventory(inventory):
        print("\nSale completed successfully!")
        print("Product:", product["name"])
        print("Quantity Sold:", old_quantity_sold)
        print("Total Amount: Rs.", f"{total:.2f}")
        print("Remaining Stock:", product["quantity"])

        if product["quantity"] <= product["min_stock"]:
            print("Warning: Product is now at low-stock level.")
    else:
        product["quantity"] = old_quantity


# Calculate total inventory value
def inventory_value(inventory):
    total = sum(
        product["price"] * product["quantity"]
        for product in inventory.values()
    )

    total_units = sum(
        product["quantity"]
        for product in inventory.values()
    )
 
    print("\n--- Inventory Summary ---")
    print("Number of Product Types:", len(inventory))
    print("Total Units in Stock:", total_units)
    print("Total Inventory Value: Rs.", f"{total:.2f}")


# Display low-stock products
def low_stock_report(inventory):
    print("\n--- Low-Stock Report ---")

    low_stock = [
        (product_id, product)
        for product_id, product in inventory.items()
        if product["quantity"] <= product["min_stock"]
    ]

    if not low_stock:
        print("No low-stock products.")
        return

    for product_id, product in low_stock:
        print(
            f"{product_id} - {product['name']} | "
            f"Quantity: {product['quantity']} | "
            f"Threshold: {product['min_stock']}"
        )


# Main menu
def main():
    inventory = load_inventory()

    while True:
        print("\n========== INVENTORY MANAGEMENT SYSTEM ==========")
        print("1. Add Product")
        print("2. View All Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Sell Product")
        print("7. Inventory Summary")
        print("8. Low-Stock Report")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            add_product(inventory)
        elif choice == "2":
            view_products(inventory)
        elif choice == "3":
            search_product(inventory)
        elif choice == "4":
            update_product(inventory)
        elif choice == "5":
            delete_product(inventory)
        elif choice == "6":
            sell_product(inventory)
        elif choice == "7":
            inventory_value(inventory)
        elif choice == "8":
            low_stock_report(inventory)
        elif choice == "9":
            print("Thank you for using the Inventory Management System!")
            break
        else:
            print("Invalid choice. Please select 1-9.")


if __name__ == "__main__":
    main()  
