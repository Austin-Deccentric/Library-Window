from window_library.register import register_user, add_new_book

def main() -> None:
    while True:
        print("\n--- BELLO'S LIBRARY ---")
        print("1. Register user")
        print("2. Add new book")
        print("3. Exit")

        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                register_user()
            elif choice == "2":
                add_new_book()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
