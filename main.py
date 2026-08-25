from window_library.storage import load_users, load_books
from window_library.utils import prompt_login
from window_library.views import library_menu



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
