from window_library.storage import load_users, load_books
from window_library.utils import log_activity, prompt_login
from window_library.verbs import post_book, delete_book
from window_library.mtypes import Book, User


def library_menu(books: list[Book], user: User) -> bool:
    """Run the library menu after a successful login."""
    while True:
        print("\n--- BELLO'S LIBRARY ---")
        print("1. Add new book")
        print("2. Delete book")
        print("3. Log out")
        print("4. Exit")

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
            elif choice == "3":
                print("Logged out.")
                return True
            elif choice == "4" or choice == "exit":
                print("Goodbye!")
                return False
            else:
                print("Invalid choice. Please select 1, 2, 3, or 4.")
        except ValueError as error:
            print(error)

def main() -> None:
    """Restart at login after three failed attempts or after logging out."""
    users = load_users()
    books = load_books()
    
    while True:
        print('\nWelcome to Bello\'s Library!')
        _ = input('Press Enter to continue.')

        flag, user = prompt_login(users)
        if not flag:   #returns True if user is found and this block is skipped, else it restarts the main loop
            continue

        should_restart = library_menu(books, user)  

        if not should_restart:  # False if user exits program so program ends
            break


if __name__ == "__main__":
    main()
