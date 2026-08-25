from window_library.mtypes import Book, User
from window_library.storage import load_users
from window_library.verbs import delete_book, post_book
from window_library.utils import log_activity


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
        print("4. Log out")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                response = post_book(books)
                if response["status_code"] in [201, 200]:
                    print(f"Book {response.get('data')['title']} added successfully with ID {response.get('data')['book_id']}.")
                    log_activity(f"Book {response.get('data')['title']} added successfully with ID {response.get('data')['book_id']} by {user['username']}.")
                else:
                    print(f"Failed to add book: {response['message']}")
                    log_activity(f"Failed to add book: {response['message']} by {user['username']}")
                    
            elif choice == "2":
                response = delete_book(books, user)
                if response["status_code"] == 200:
                    print(f"Book {response.get('data')['title']} deleted successfully.")
                    log_activity(f"Book: {response.get('data')['title']} deleted successfully by {user['username']}.")
                else:
                    print(f"Failed to delete book: {response['message']}")
                    log_activity(f"Failed to delete book: {response['message']} by {user['username']}")
            
            elif choice == "4":
                print("Logged out.")
                return True
                
            elif choice == "5" or choice == "exit":
                print("Goodbye!")
                return False
            else:
                print("Invalid choice. Please select 1, 2, 3,4 or 5.")
        except ValueError as error:
            print(error)




if __name__ == "__main__":
    view_staff()