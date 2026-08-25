from window_library.storage import load_books, load_users


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


def view_books() -> None:
    """Display all book records."""
    books = load_books()

    print("\n--- BOOKS ---")
    if not books:
        print("No book records found.")
        return

    for book in books:
        print(f"ID: {book['book_id']}")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Status: {book['status']}")
        print("-" * 30)

if __name__ == "__main__":
    view_books()
    view_staff()