from window_library.mtypes import Book, ResponseObject, User
from window_library.storage import add_book, save_books
from window_library.utils import is_chief


# --- Pure core (no I/O) ---

def get_book_by_id(books: list[Book], book_id: int) -> ResponseObject:
    """Pure lookup by ID — no input()."""
    for book in books:
        if book["book_id"] == book_id:
            return {
                "status_code": 200,
                "message": "Done, here you go",
                "data": book,
            }
    return {
        "status_code": 404,
        "message": "There is no such book",
        "data": None,
    }


def create_book(
    books: list[Book], title: str, author: str, status: str = "on shelf"
) -> ResponseObject:
    """Pure book creation — validates and saves. Raises ValueError on bad input."""
    title = title.strip()
    author = author.strip()
    status = status.strip().lower() or "on shelf"

    if not title or not author:
        raise ValueError("Title or author cannot be empty.")
    if status not in ("on shelf", "borrowed"):
        raise ValueError("Invalid status. Use 'on shelf' or 'borrowed'.")

    next_book_id: int = max((b["book_id"] for b in books), default=0) + 1
    book: Book = {
        "book_id": next_book_id,
        "title": title,
        "author": author,
        "status": status,
    }
    add_book(books, book)
    return {
        "status_code": 201,
        "message": "Book added successfully",
        "data": book,
    }


def update_book(
    books: list[Book],
    book_id: int,
    user: User,
    title: str | None = None,
    author: str | None = None,
    status: str | None = None,
) -> ResponseObject:
    """Pure update by ID — validates and saves. Raises ValueError on bad status."""
    response = get_book_by_id(books, book_id)
    if response["status_code"] != 200 or response["data"] is None:
        return response

    book = response["data"]
    assert isinstance(book, dict)

    # Validate status only for Chief Librarian; ignore otherwise
    if status is not None and is_chief(user):
        status = status.strip().lower()
        if status not in ("on shelf", "borrowed"):
            raise ValueError("Invalid status. Use 'on shelf' or 'borrowed'.")
        book["status"] = status

    if title is not None and title.strip():
        book["title"] = title.strip()
    if author is not None and author.strip():
        book["author"] = author.strip()

    save_books(books)
    return {
        "status_code": 200,
        "message": "Book updated successfully",
        "data": book,
    }


def delete_book_by_id(books: list[Book], book_id: int, user: User) -> ResponseObject:
    """Pure delete by ID — no input()."""
    if not is_chief(user):
        return {
            "status_code": 403,
            "message": "Only chief librarians can delete books",
            "data": None,
        }
    for index, book in enumerate(books):
        if book["book_id"] == book_id:
            _ = books.pop(index)
            save_books(books)
            return {
                "status_code": 200,
                "message": "Book deleted successfully",
                "data": book,
            }
    return {
        "status_code": 404,
        "message": "Book not found",
        "data": None,
    }


# --- I/O wrappers (thin, keep existing signatures for views.py) ---

def get_book(books: list[Book], prompt: str = "Enter book ID: ") -> ResponseObject:
    """Prompt wrapper — reads ID and delegates to get_book_by_id."""
    raw = input(prompt)
    try:
        book_id = int(raw)
    except ValueError:
        return {
            "status_code": 400,
            "message": "Invalid book ID",
            "data": None,
        }
    return get_book_by_id(books, book_id)


def get_books(books: list[Book]) -> ResponseObject:
    """Display all book records."""
    print("\n--- BOOKS ---")
    if not books:
        return {
            "status_code": 404,
            "message": "No books found",
            "data": None,
        }

    for book in books:
        print(f"ID: {book['book_id']}")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Status: {book['status']}")
        print("-" * 30)

    return {
        "status_code": 200,
        "message": "Done, here you go",
        "data": books,
    }


def post_book(books: list[Book]) -> ResponseObject:
    """Collect new-book details, assign the next ID, and save the book."""
    title = input("Enter book title: ").strip()
    author = input("Enter author: ").strip()
    status = input("Enter status (on shelf/borrowed): ").strip().lower() or "on shelf"
    return create_book(books, title, author, status)


def put_book(books: list[Book], user: User) -> ResponseObject:
    """Update an existing book's details (prompt wrapper)."""
    response = get_book(books, "Enter book ID to update: ")
    if response["status_code"] != 200 or response["data"] is None:
        return response

    book = response["data"]
    assert isinstance(book, dict)
    book_id = book["book_id"]

    title = input("Enter new title: ").strip()
    author = input("Enter new author: ").strip()
    status: str | None = None
    if is_chief(user):
        status = input("Enter new status (on shelf/borrowed): ").strip().lower() or book["status"]

    # Delegate to pure core; let ValueError propagate to views.py handler
    return update_book(
        books,
        book_id,
        user,
        title=title if title else None,
        author=author if author else None,
        status=status,
    )


def delete_book(books: list[Book], user: User) -> ResponseObject:
    """Delete a book from the library (prompt wrapper)."""
    raw = input("Enter book ID to delete: ").strip()
    try:
        book_id = int(raw)
    except ValueError:
        return {
            "status_code": 400,
            "message": "Invalid book ID",
            "data": None,
        }
    return delete_book_by_id(books, book_id, user)
