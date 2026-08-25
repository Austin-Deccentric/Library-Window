import json
from json.decoder import JSONDecodeError
from pathlib import Path
from .mtypes import Book, User

PROJECT_ROOT = Path(__file__).resolve().parent.parent
USERS_FILE = PROJECT_ROOT / "staff.json"
BOOKS_FILE = PROJECT_ROOT / "books.json"


def _load_records(filepath: str | Path) -> list[dict]:
    """Load JSON records, returning an empty list when the file is missing or invalid."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            if data is None:
                return []
            return data
    except FileNotFoundError:
        return []
    except JSONDecodeError as error:
        print(f"The file is corrupted: {error.msg}")
        return []


def _save_records(records: list[dict], filepath: str | Path) -> None:
    """Write records to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def load_users(filepath: str | Path = USERS_FILE) -> list[User]:
    """Load user records from staff.json."""
    return _load_records(filepath)  


def save_users(users: list[User], filepath: str | Path = USERS_FILE) -> None:
    """Save user records to staff.json."""
    _save_records(users, filepath)


def load_books(filepath: str | Path = BOOKS_FILE) -> list[Book]:
    """Load book records from books.json."""
    return _load_records(filepath)  


def save_books(books: list[Book], filepath: str | Path = BOOKS_FILE) -> None:
    """Save book records to books.json."""
    _save_records(books, filepath)


def add_user(
    users: list[User], user: User, filepath: str | Path = USERS_FILE
) -> None:
    """Append a user to the list and save the updated user records."""
    users.append(user)
    save_users(users, filepath)


def add_book(
    books: list[Book], book: Book, filepath: str | Path = BOOKS_FILE
) -> None:
    """Append a book to the list and save the updated book records."""
    books.append(book)
    save_books(books, filepath)



