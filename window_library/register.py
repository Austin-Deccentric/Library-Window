from window_library.mtypes import Book, User
from window_library.storage import add_book, add_user, load_books, load_users
from window_library.utils import find_member


def register_user() -> None:
    """Collect a new user's details and save the user when the username is available."""
    users = load_users()
    username = input("Enter username: ").strip()

    if not username:
        raise ValueError("Username cannot be empty.")

    if find_member(users, username):
        raise ValueError("That username is already registered.")

    password = input("Enter password: ").strip()
    position = input("Enter position (Member/Chief Librarian): ").strip() or "Member"
    if position not in ("Member", "Chief Librarian"):
        raise ValueError("Invalid position. Use 'Member' or 'Chief Librarian'.")

    user: User = {
        "username": username,
        "password": password,
        "position": position,
    }
    add_user(users, user)
    print(f"User '{username}' registered successfully.")



