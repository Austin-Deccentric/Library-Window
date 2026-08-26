# Bello's Library Window

A command-line library management application built with Python. It lets registered staff log in, view the book catalogue, add books, retrieve individual books, and manage deletions based on staff role.

## Features

- Secure username-and-password login with a maximum of three attempts
- View all books in the catalogue
- Retrieve a book by its ID
- Add a new book with title, author, and availability status
- Update an existing book
- Delete books (Chief Librarian only)
- Log successful and failed actions to `log.txt`
- Log out and sign in as another user without restarting the program


## Menu options

| Option | Action | Details |
|---|---|---|
| 1 | Add new book | Creates and saves a book with the next available ID |
| 2 | Delete book | Removes a book; restricted to `Chief Librarian` users |
| 3 | Update book | Updates a book’s title and author; Chief Librarians can also update its status |
| 4 | Get book | Finds and displays one book using its ID |
| 5 | Get books | Displays every book in the catalogue |
| 6 | Log out | Returns to the login screen |
| 7 | Exit | Closes the application |


## Project structure

```text
Bello's Library Window/
├── main.py                    # Application entry point
├── books.json                 # Persistent book catalogue
├── staff.json                 # Staff login records and roles
├── log.txt                    # Activity log generated while the app runs
├── pyproject.toml             # Project metadata and Python requirement
└── window_library/
    ├── __init__.py
    ├── mtypes.py              # Type definitions
    ├── storage.py             # JSON loading and saving operations
    ├── utils.py               # Login and activity logging helpers
    ├── verbs.py               # Book actions: create, retrieve, delete
    └── views.py               # Command-line menu and display logic

## Using the application

1. Start the program and press Enter at the welcome screen.
2. Sign in with a username and password stored in `staff.json`.
3. Choose a menu option from 1 to 7.
4. Follow the prompts for book information or a book ID.
5. Select option 6 to log out, or option 7 to exit.

When you choose option 5, the program displays the catalogue and waits for you to press Enter before returning to the menu.

## Updating a book

1. Select option 3, **Update book**.
2. Enter the ID of the book you want to edit.
3. Enter a new title and/or author; leave either field blank to keep its current value.
4. If you are a `Chief Librarian`, you can also change the status to `on shelf` or `borrowed`.
5. The updated book is saved to `books.json`.

## Roles and permissions

Any valid staff member can view, add, retrieve, and update a book’s title or author. Only a user whose position is `Chief Librarian` can delete a book or update its availability status. [cite:10]
