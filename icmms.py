"""
KITT Industries - Intelligent Car Manufacturing Management System (ICMMS)

A menu-driven Python application that allows staff to manage car records,
organise vehicle data, perform sorting operations, and quickly search for
specific cars. All records are stored in a simple JSON text file so that
no data is lost when the program exits.

Author: KITT Industries
"""

import json
import re
from pathlib import Path

FILE_NAME = "car_inventory.json"


def load_inventory():
    """Load car records from the JSON storage file."""
    path = Path(FILE_NAME)
    if path.exists():
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_inventory(cars):
    """Save all car records to the JSON storage file."""
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(cars, file, indent=4)


def validate_car_id(cars, car_id):
    """Return True if the Car ID has a valid format and is not a duplicate."""
    # A valid ID must start with letters and end with digits (e.g. C101).
    if not re.fullmatch(r"[A-Za-z]+\d+", car_id):
        print("Invalid Car ID. Use letters followed by digits, e.g. C101.")
        return False
    if any(car["id"].upper() == car_id.upper() for car in cars):
        print("Car ID already exists. Please use a different ID.")
        return False
    return True


def validate_price():
    """Prompt for a price and return it only if it is a positive number."""
    while True:
        try:
            price = float(input("Enter Price: "))
            if price <= 0:
                print("Price must be a positive number.")
                continue
            return price
        except ValueError:
            print("Invalid price. Please enter a number.")


def validate_category():
    """Prompt for a category and return it only if it is valid text."""
    while True:
        category = input("Enter Category (e.g. Autonomous, AI-Enabled, Electric): ").strip()
        if category and category.replace(" ", "").isalpha():
            return category
        print("Invalid category. Use letters only (no numbers or symbols).")


def display_cars(cars):
    """Display every car record in a readable table."""
    if not cars:
        print("No cars available.")
        return

    print("-" * 64)
    print(f"{'ID':<10}{'Name':<20}{'Category':<15}{'Price':>10}")
    print("-" * 64)

    for car in cars:
        print(f"{car['id']:<10}{car['name']:<20}{car['category']:<15}{car['price']:>10.2f}")


def add_car(cars):
    """Add a new car record after validating all input values."""
    car_id = input("Enter Car ID: ").strip().upper()

    if not validate_car_id(cars, car_id):
        return

    name = input("Enter Car Name: ").strip()
    if not name:
        print("Car name cannot be empty.")
        return

    category = validate_category()
    price = validate_price()

    cars.append({
        "id": car_id,
        "name": name,
        "category": category,
        "price": price
    })

    print("Car added successfully.")


def update_car(cars):
    """Update the name, category, and price of an existing car record."""
    car_id = input("Enter Car ID to update: ").strip().upper()

    for car in cars:
        if car["id"] == car_id:
            new_name = input(f"Current name: {car['name']}. New name (press Enter to keep): ").strip()
            if new_name:
                car["name"] = new_name

            new_category = input(
                f"Current category: {car['category']}. New category (press Enter to keep): ").strip()
            if new_category and new_category.replace(" ", "").isalpha():
                car["category"] = new_category
            elif new_category:
                print("Invalid category. Keeping the current value.")

            update_price = input(f"Current price: {car['price']}. Update price? (y/n): ").strip().lower()
            if update_price == "y":
                car["price"] = validate_price()

            print("Car record updated successfully.")
            return

    print("Car not found.")


def delete_car(cars):
    """Remove an existing car record by its Car ID."""
    car_id = input("Enter Car ID to delete: ").strip().upper()

    for car in cars:
        if car["id"] == car_id:
            cars.remove(car)
            print("Car record deleted successfully.")
            return

    print("Car not found.")


def search_car(cars):
    """Search for a single car record by its Car ID."""
    car_id = input("Enter Car ID to search: ").strip().upper()

    for car in cars:
        if car["id"] == car_id:
            print(f"ID: {car['id']}, Name: {car['name']}, "
                  f"Category: {car['category']}, Price: {car['price']}")
            return

    print("Car not found.")


def sort_by_price_asc(cars):
    """Display all cars sorted by price in ascending order."""
    display_cars(sorted(cars, key=lambda car: car["price"]))


def sort_by_id_desc(cars):
    """Display all cars sorted by Car ID in descending order."""
    display_cars(sorted(cars, key=lambda car: car["id"], reverse=True))


def generate_report(cars):
    """Print a summary report with inventory statistics."""
    if not cars:
        print("No data available to generate a report.")
        return

    total_cars = len(cars)
    total_value = sum(car["price"] for car in cars)
    average_price = total_value / total_cars
    cheapest = min(cars, key=lambda car: car["price"])
    most_expensive = max(cars, key=lambda car: car["price"])

    print("\n========== INVENTORY SUMMARY REPORT ==========")
    print(f"Total number of cars:          {total_cars}")
    print(f"Total inventory value:         ${total_value:,.2f}")
    print(f"Average price:                 ${average_price:,.2f}")
    print(f"Cheapest car:                  {cheapest['name']} (${cheapest['price']:,.2f})")
    print(f"Most expensive car:            {most_expensive['name']} (${most_expensive['price']:,.2f})")
    print("==============================================")


def main():
    """Run the main menu loop of the ICMMS application."""
    cars = load_inventory()

    while True:
        print("\n======== KITT ICMMS MAIN MENU ========")
        print("1. Display all cars")
        print("2. Add a new car")
        print("3. Update a car record")
        print("4. Delete a car record")
        print("5. Search a car by ID")
        print("6. Sort cars by price (ascending)")
        print("7. Sort cars by ID (descending)")
        print("8. Generate inventory summary report")
        print("9. Save and Exit")
        print("======================================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_cars(cars)
        elif choice == "2":
            add_car(cars)
            save_inventory(cars)  # Save immediately to prevent data loss.
        elif choice == "3":
            update_car(cars)
            save_inventory(cars)
        elif choice == "4":
            delete_car(cars)
            save_inventory(cars)
        elif choice == "5":
            search_car(cars)
        elif choice == "6":
            sort_by_price_asc(cars)
        elif choice == "7":
            sort_by_id_desc(cars)
        elif choice == "8":
            generate_report(cars)
        elif choice == "9":
            save_inventory(cars)
            print("All records saved. Thank you for using KITT ICMMS. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 9.")


if __name__ == "__main__":
    main()
