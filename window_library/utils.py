from .mtypes import Book, User

def find_book(books: list[Book], book_id: int) -> Book | None:
    """Return the book matching the supplied book ID, or None if not found."""
    for book in books:
        if book["book_id"] == book_id:
            return book
    return None


def find_member(users: list[User], username: str) -> User | None:
    """Return the user matching the supplied username, or None if not found."""
    for user in users:
        if user["username"] == username:
            return user
    return None


def login_user(users: list[User], username:str, password:str) -> User | None:
    """Return the user matching the supplied username and password, or None if not found."""
    user = find_member(users, username)
    if user and check_password(user, password):
        return user
    return None


def check_password(user: User, password: str) -> bool:
    """Return True if the user's password matches the supplied password, False otherwise."""
    return user["password"] == password