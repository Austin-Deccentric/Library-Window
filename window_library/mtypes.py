from typing import TypedDict

class User(TypedDict):
    username: str
    password: str
    position: str

class Book(TypedDict):
    book_id: int
    title: str
    author: str
    status: str

class ResponseObject(TypedDict):
    status_code: int
    message: str
    data: Book | list[Book] | None