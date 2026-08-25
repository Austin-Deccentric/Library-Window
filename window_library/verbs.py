from window_library.mtypes import Book, ResponseObject, User
from window_library.storage import add_book, load_books


def get_book(books: list[Book]) -> ResponseObject:
    """Return the book matching the supplied book ID, or None if not found."""
    book_id = input('Enter book Id to update: ')
    try:
        book_id = int(book_id)
    except ValueError:
        return {
            "status_code": 400,
            "message": "Invalid book ID",
            "data": None,
        }
        
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

    if not title or not author:
        raise ValueError("Title or author cannot be empty.")

    status = input("Enter status (on shelf/borrowed): ").strip().lower() or "on shelf"
    if status not in ("on shelf", "borrowed"):
        raise ValueError("Invalid status. Use 'on shelf' or 'borrowed'.")

    next_book_id: int = max((book["book_id"] for book in books), default=0) + 1
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

    
def put_book(books: list[Book], user: User) -> ResponseObject:
    """Update an existing book's details."""
    response = get_book(books)
    if response["status_code"] != 200:
        return response
        
    book = response["data"]
    title = input("Enter new title: ").strip()
    author = input("Enter new author: ").strip()
    if user["position"] == "Chief Librarian":
        status = input("Enter new status (on shelf/borrowed): ").strip().lower() or book["status"]
        if status not in ("on shelf", "borrowed"):
            raise ValueError("Invalid status. Use 'on shelf' or 'borrowed'.")
    if title:
        book["title"] = title
    if author:
        book["author"] = author
    if user["position"] == "Chief Librarian":
        book["status"] = status
        
    
    return {
        "status_code": 200,
        "message": "Book updated successfully",
        "data": book,
    }


def delete_book(books: list[Book], user: User) -> ResponseObject:
    """Delete a book from the library."""
    if user["position"] != "Chief Librarian":
        return {
            "status_code": 403,
            "message": "Only chief librarians can delete books",
            "data": None,
        }
    # response = get_book(books)
    # if response["status_code"] != 200:
    #     return response
    # book = response["data"]
    
    # book = next((b for b in books if b["book_id"] == book_id), None)
    # if not book:
    #     return {
    #         "status_code": 404,
    #         "message": "Book not found",
    #         "data": None,
    #     }
    try:
        book_id = int(input("Enter book ID to delete: "))
        for index, book in enumerate(books):
            if book["book_id"] == book_id:
                books.pop(index)
        return {
            "status_code": 200,
            "message": "Book deleted successfully",
            "data": book,
        }
    except ValueError:
        return {
            "status_code": 404,
            "message": "Deletion failed",
            "data": None,
        }