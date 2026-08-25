from window_library.register import register_user, add_new_book
from window_library.storage import load_users
from window_library.utils import login_user
from window_library.mtypes import User

MAX_LOGIN_ATTEMPTS = 3


def prompt_login(users: list[User]) -> bool:
    """Prompt for login credentials up to three times."""
   
    for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
        print(f"\n--- LOGIN ({attempt}/{MAX_LOGIN_ATTEMPTS}) ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        user = login_user(users, username, password)

        if user:
            print(f"Welcome, {user['username']}!")
            return True

        remaining_attempts = MAX_LOGIN_ATTEMPTS - attempt
        if remaining_attempts:
            print(f"Invalid username or password. {remaining_attempts} attempts remaining.")

    print("Maximum login attempts reached.")
    return False


def library_menu() -> bool:
    """Run the library menu after a successful login."""
    while True:
        print("\n--- BELLO'S LIBRARY ---")
        print("1. Add new book")
        print("2. Log out")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                add_new_book()
            elif choice == "2":
                print("Logged out.")
                return True
            elif choice == "3":
                print("Goodbye!")
                return False
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError as error:
            print(error)

def main() -> None:
    """Restart at login after three failed attempts or after logging out."""
    users = load_users()
    
    while True:
        if not prompt_login(users):
            continue

        should_restart = library_menu()

        if not should_restart:
            break


if __name__ == "__main__":
    main()
