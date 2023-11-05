from telegram_utils import TelegramClient

if __name__ == "__main__":
    api_id = int(input("Enter your API id: "))
    api_hash = input("Enter your API hash: ")

    client = TelegramClient(api_id, api_hash)

    while True:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("1. Get data from Telegram channel")
        print("2. Print current data")
        print("3. Make a backup of the database")
        print("4. Upload database backup")
        print("5. Clear all data")
        print("6. Exit")
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            chat_id = input("Enter chat id: ")
            n = int(input("Enter the number of posts: "))
            date = input("Enter the date (YYYY-MM-DD): ")
            client.get_n_last_posts(chat_id, n, date)
        elif choice == 2:
            client.print_data()
        elif choice == 3:
            client.backup_db()
        elif choice == 4:
            client.restore_db()
        elif choice == 5:
            client.clear_data()
        elif choice == 6:
            client.conn.close()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
            time.sleep(1)
            continue