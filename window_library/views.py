from window_library.mtypes import Book, User
from window_library.storage import load_users
from window_library.utils import log_activity
from window_library.verbs import delete_book, get_book, get_books, post_book, put_book


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


def _handle_response(
    response: dict,
    user: User,
    success_action: str,
    failure_action: str,
) -> None:
    """Centralized print + log for book actions to keep menu DRY."""
    book = response.get("data")
    code = response["status_code"]
    if code in (200, 201) and isinstance(book, dict):
        title = book.get("title")
        if success_action == "added":
            print(f"Book {title} added successfully with ID {book.get('book_id')}.")
        elif success_action == "deleted":
            print(f"Book {title} deleted successfully.")
        elif success_action == "updated":
            print(f"Book {title} updated successfully.")
        elif success_action == "retrieved":
            print(f"\nBook: {title}\nAuthor: {book.get('author')}\nStatus: {book.get('status')}")
        log_activity(
            f"Book: {title} {success_action} successfully by {user['username']} with response code: {code}."
            if success_action != "added"
            else f"Book {title} added successfully with ID {book.get('book_id')} and response code: {code} by {user['username']}."
        )
    else:
        msg = response["message"]
        print(f"Failed to {failure_action}: {msg}")
        log_activity(
            f"Failed to {failure_action}: {msg} by {user['username']} with response code: {code}"
        )


def library_menu(books: list[Book], user: User | None) -> bool:
    """Run the library menu after a successful login."""
    if user is None:
        return True

    while True:
        print("\n--- BELLO'S LIBRARY ---")
        print("1. Add new book")
        print("2. Delete book")
        print("3. Update book")
        print("4. Get book")
        print("5. Get books")
        print("6. Log out")
        print("7. Exit")

        choice = input("Choose an option: ").strip().lower()

        try:
            if choice == "1":
                response = post_book(books)
                _handle_response(response, user, "added", "add book")

            elif choice == "2":
                response = delete_book(books, user)
                _handle_response(response, user, "deleted", "delete book")

            elif choice == "3":
                response = put_book(books, user)
                _handle_response(response, user, "updated", "update book")

            elif choice == "4":
                response = get_book(books)
                _handle_response(response, user, "retrieved", "get book")

            elif choice == "5":
                response = get_books(books)
                if response["status_code"] == 200:
                    log_activity(
                        f"Books retrieved successfully by {user['username']} with response code: {response['status_code']}."
                    )
                    _ = input("\nPress Enter to return to the menu...")
                else:
                    print(f"Failed to get books: {response['message']}")
                    log_activity(
                        f"Failed to get books: {response['message']} by {user['username']} with response code: {response['status_code']}"
                    )

            elif choice == "6":
                print("Logged out.")
                return True

            elif choice == "7" or choice == "exit":
                print("Goodbye!")
                return False
            else:
                print("Invalid choice. Please select 1-7 or type 'exit'.")
        except ValueError as error:
            print(error)
            log_activity(
                f"Failed to process request: {error} by {user['username']} with response code: 400"
            )


if __name__ == "__main__":
    view_staff()
