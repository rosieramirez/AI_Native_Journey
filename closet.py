import json
import os

FILENAME = "closet_inventory.json"

def load_inventory():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return []

def save_inventory(inventory):
    with open(FILENAME, "w") as f:
        json.dump(inventory, f, indent=4)

def add_closet_item():
    item = {}
    item["name"] = input("Item name: ")
    item["category"] = input("Category (e.g., Top, Dress, Shoes): ")
    item["color"] = input("Color: ")
    item["size"] = input("Size (e.g., S, M, L, 6.5): ")
    item["brand"] = input("Brand (optional): ")
    item["image_file"] = input("Image filename (optional): ")
    tags_input = input("Enter tags separated by commas (e.g., vintage,event,date-night): ")
    item["tags"] = [tag.strip().lower() for tag in tags_input.split(",") if tag.strip()]

    inventory = load_inventory()
    inventory.append(item)
    save_inventory(inventory)
    print("Item added to closet.")

def view_inventory():
    inventory = load_inventory()
    if not inventory:
        print("Closet is empty.")
        return
    for index, item in enumerate(inventory, start=1):
        print(f"\nItem {index}:")
        for key, value in item.items():
            if isinstance(value, list):
                print(f"{key}: {', '.join(value)}")
            else:
                print(f"{key}: {value}")

def search_inventory():
    tag = input("Enter tag to search by (e.g., vintage): ").strip().lower()
    inventory = load_inventory()
    results = [item for item in inventory if "tags" in item and tag in item["tags"]]
    if results:
        print(f"\nItems tagged with '{tag}':")
        for index, item in enumerate(results, start=1):
            print(f"\nItem {index}:")
            for key, value in item.items():
                if isinstance(value, list):
                    print(f"{key}: {', '.join(value)}")
                else:
                    print(f"{key}: {value}")
    else:
        print(f"No items found with tag '{tag}'.")

def run():
    print("Closet Inventory Tool")
    while True:
        choice = input("\nWhat would you like to do? (add/view/search/exit): ").strip().lower()
        if choice == "add":
            add_closet_item()
        elif choice == "view":
            view_inventory()
        elif choice == "search":
            search_inventory()
        elif choice == "exit":
            print("Exiting program.")
            break
        else:
            print("Invalid input. Please enter 'add', 'view', 'search', or 'exit'.")

if __name__ == "__main__":
    run()
