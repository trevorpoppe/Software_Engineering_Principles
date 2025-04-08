def main():
    db_name = 'bookkeeper.db'
    print("Choose mode:")
    print("1: CLI Mode")
    print("2: AI Chat Mode")

    choice = input("Enter 1 or 2: ").strip()
    if choice == '1':
        start_cli(db_name)
    elif choice == '2':
        ai_interaction(db_name)
    else:
        print("Invalid choice. Exiting.")
