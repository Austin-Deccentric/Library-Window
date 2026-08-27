from datetime import datetime
from window_library.mtypes import User




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

def prompt_login(users: list[User]) -> tuple[bool, User | None]:
    """Prompt for login credentials up to three times."""
    MAX_LOGIN_ATTEMPTS = 3
   
    for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
        print(f"\n--- LOGIN ({attempt}/{MAX_LOGIN_ATTEMPTS}) ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        user = login_user(users, username, password)

        if user:
            print(f"Welcome, {user['username']}!")
            return (True, user)

        remaining_attempts = MAX_LOGIN_ATTEMPTS - attempt
        if remaining_attempts:
            print(f"Invalid username or password. {remaining_attempts} attempts remaining.")

    print("Maximum login attempts reached.")
    return (False, None)

def log_activity(activity: str, filepath: str = "log.txt") -> None:
    """Append a timestamped activity record to the application log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filepath, "a", encoding="utf-8") as file:
        _ = file.write(f"[{timestamp}] {activity}\n")