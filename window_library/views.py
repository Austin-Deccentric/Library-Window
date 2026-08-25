from window_library.storage import load_users


def view_staff() -> None:
    """Display all staff and member records."""
    users = load_users()

    print("\n--- STAFF AND MEMBERS ---")
    if not users:
        print("No staff or member records found.")
        return

    for user in users:
        print(f"Username: {user['username']}")
        print(f"Position: {user['position']}")
        print("-" * 30)




if __name__ == "__main__":
    view_staff()