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


def library_menu(books: list[Book], user: User | None) -> bool:
    """Run the library menu after a successful login."""
    if user:
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
                    book = response.get("data")
                    
                    if response["status_code"] in [201, 200] and isinstance(book, dict):
                        print(
                            f"Book {book.get('title')} added successfully with ID {book.get('book_id')}."
                        )
                        log_activity(
                            f"Book {book.get('title')} added successfully with ID {book.get('book_id')} and response code: {response['status_code']} by {user['username']}."
                        )
                    else:
                        print(f"Failed to add book: {response['message']}")
                        log_activity(
                            f"Failed to add book: {response['message']} with response code: {response['status_code']} by {user['username']}"
                        )
    
                elif choice == "2":
                    response = delete_book(books, user)
                    book = response.get("data")
                    if response["status_code"] == 200 and isinstance(book, dict):
                        print(f"Book {book.get('title')} deleted successfully.")
                        log_activity(
                            f"Book: {book.get('title')} deleted successfully by {user['username']} with response code: {response['status_code']}."
                        )
                    else:
                        print(f"Failed to delete book: {response['message']}")
                        log_activity(
                            f"Failed to delete book: {response['message']} by {user['username']} with response code: {response['status_code']}"
                        )
    
                elif choice == "3":
                    response = put_book(books, user)
                    book = response.get("data")
                    if response["status_code"] == 200 and isinstance(book, dict):
                        print(f"Book {book.get('title')} updated successfully.")
                        log_activity(
                            f"Book: {book.get('title')} updated successfully by {user['username']} with response code: {response['status_code']}."
                        )
                    else:
                        print(f"Failed to update book: {response['message']}")
                        log_activity(
                            f"Failed to update book: {response['message']} by {user['username']} with response code: {response['status_code']} "
                        )
    
                elif choice == "4":
                    response = get_book(books)
                    book = response.get("data")
                    if response["status_code"] == 200 and isinstance(book, dict):
                        print(
                            f"\nBook: {book.get('title')}\nAuthor: {book.get('author')}\nStatus: {book.get('status')}"
                        )
                        log_activity(
                            f"Book: {book.get('title')} retrieved successfully by {user['username']} with response code: {response['status_code']}."
                        )
                    else:
                        print(f"Failed to get book: {response['message']}")
                        log_activity(
                            f"Failed to get book: {response['message']} by {user['username']} with response code: {response['status_code']}."
                        )
    
                elif choice == "5":
                    response = get_books(books)
                    # books = response.get('data')
                    if response["status_code"] == 200:
                        log_activity(f"Books retrieved successfully by {user['username']} with response code: {response['status_code']} .")
                        _ = input("\nPress Enter to return to the menu...")
                    else:
                        print(f"Failed to get books: {response['message']}")
                        log_activity(
                            f"Failed to get books: {response['message']} by {user['username']} with response code: {response['status_code']} "
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
    else:
        return True


if __name__ == "__main__":
    view_staff()
