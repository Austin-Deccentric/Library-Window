from window_library.mtypes import Book, User
from window_library.storage import load_users
from window_library.utils import log_activity
from window_library.verbs import delete_book, get_book, get_books, post_book


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


def library_menu(books: list[Book], user: User) -> bool:
    """Run the library menu after a successful login."""
    while True:
        print("\n--- BELLO'S LIBRARY ---")
        print("1. Add new book")
        print("2. Delete book")
        print("3. Get book")
        print("4. Get books")
        print("5. Log out")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                response = post_book(books)
                if response["status_code"] in [201, 200]:
                    print(
                        f"Book {response.get('data')['title']} added successfully with ID {response.get('data')['book_id']}."
                    )
                    log_activity(
                        f"Book {response.get('data')['title']} added successfully with ID {response.get('data')['book_id']} by {user['username']}."
                    )
                else:
                    print(f"Failed to add book: {response['message']}")
                    log_activity(
                        f"Failed to add book: {response['message']} by {user['username']}"
                    )

            elif choice == "2":
                response = delete_book(books, user)
                book = response.get("data")
                if response["status_code"] == 200:
                    print(f"Book {book['title']} deleted successfully.")
                    log_activity(
                        f"Book: {book['title']} deleted successfully by {user['username']}."
                    )
                else:
                    print(f"Failed to delete book: {response['message']}")
                    log_activity(
                        f"Failed to delete book: {response['message']} by {user['username']}"
                    )

            elif choice == "3":
                response = get_book(books)
                book = response.get("data")
                if response["status_code"] == 200:
                    print(
                        f"\nBook: {book['title']}\nAuthor: {book['author']}\nStatus: {book['status']}"
                    )
                    log_activity(
                        f"Book: {book['title']} retrieved successfully by {user['username']}."
                    )
                else:
                    print(f"Failed to get book: {response['message']}")
                    log_activity(
                        f"Failed to get book: {response['message']} by {user['username']}"
                    )

            elif choice == "4":
                response = get_books(books)
                # books = response.get('data')
                if response["status_code"] == 200:
                    log_activity(f"Books retrieved successfully by {user['username']}.")
                    input("\nPress Enter to return to the menu...")
                else:
                    print(f"Failed to get books: {response['message']}")
                    log_activity(
                        f"Failed to get books: {response['message']} by {user['username']}"
                    )

            elif choice == "5":
                print("Logged out.")
                return True

            elif choice == "6" or choice == "exit":
                print("Goodbye!")
                return False
            else:
                print("Invalid choice. Please select 1, 2, 3,4, 5 or 6.")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    view_staff()
