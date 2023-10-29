from pyrogram import Client
from datetime import datetime
import sqlite3
import os
import time
import glob

class TelegramClient:
    def __init__(self, api_id, api_hash):
        self.app = Client('my_account', api_id=api_id, api_hash=api_hash)
        self.conn = sqlite3.connect('telegram_data.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.media_id_counter = 0
        self.reaction_id_counter = 0

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS channels
                               (channel_id INTEGER, channel_name TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                               (post_id INTEGER, channel_id INTEGER, post_text TEXT, views INTEGER, time TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS media
                               (media_id INTEGER, post_id INTEGER, media_type TEXT, file_id TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reactions
                               (reaction_id INTEGER, post_id INTEGER, emoji TEXT, count INTEGER)''')
        self.conn.commit()

    def save_media(self, message):
        if not os.path.exists('data'):
            os.makedirs('data')
        file_id = message.photo.file_id if message.photo is not None else message.video.file_id
        file_path = self.app.download_media(file_id)

        channel_id = message.chat.id
        date = message.date  
        directory = os.path.join('data', str(channel_id), str(date.year), str(date.month), str(date.day))

        os.makedirs(directory, exist_ok=True)

        new_file_path = os.path.join(directory, os.path.basename(file_path))
        os.rename(file_path, new_file_path)

    def get_n_last_posts(self, chat_id, n, date = ''):
        if date == '':
            date = datetime.now()
        else:
            date = datetime.strptime(date, "%Y-%m-%d")
        with self.app:
            messages = list(self.app.get_chat_history(chat_id, limit=10*n, offset_date=date))
            i = 0
            media_group = None
            post_text = None
            reactions = []
            for message in messages:
                if (media_group is None or 
                    message.media_group_id is None or 
                    message.media_group_id != media_group):
                    if (i == n): break

                    if post_text is not None:
                        self.cursor.execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?)", (i, channel_id, post_text, message.views, message.date))
                        for reaction in reactions:
                            self.cursor.execute("INSERT INTO reactions VALUES (?, ?, ?, ?)", (self.reaction_id_counter, i, reaction.emoji, reaction.count))
                            self.reaction_id_counter += 1
                        i += 1

                    channel_id = message.chat.id
                    channel_name = message.chat.title
                    self.cursor.execute("INSERT INTO channels VALUES (?, ?)", (channel_id, channel_name))
                    post_text = message.text if message.text is not None else message.caption
                    reactions = message.reactions.reactions if message.reactions is not None else []
                    media_group = message.media_group_id if message.media_group_id is not None else None
                else:
                    if message.text is not None or message.caption is not None:
                        post_text = message.text if message.text is not None else message.caption
                    if message.reactions is not None:
                        reactions.extend(message.reactions.reactions)

                if message.photo is not None:
                    self.save_media(message)
                    self.cursor.execute("INSERT INTO media VALUES (?, ?, ?, ?)", (self.media_id_counter, i, 'photo', message.photo.file_id))
                    self.media_id_counter += 1
                elif message.video is not None:
                    self.save_media(message)
                    self.cursor.execute("INSERT INTO media VALUES (?, ?, ?, ?)", (self.media_id_counter, i, 'video', message.video.file_id))
                    self.media_id_counter += 1    

    def save_data(self):
        self.conn.commit()

    def print_data(self):
        self.cursor.execute("SELECT * FROM posts ORDER BY post_id DESC")
        posts = self.cursor.fetchall()

        for post in posts:
            print(f"Post {post[0]}:")
            self.cursor.execute(f"SELECT channel_id FROM channels WHERE channel_id = {post[1]}")
            print(f"Channel: {self.cursor.fetchone()[0]}")
            print(f"Text: {post[2]}")
            print(f"Views: {post[3]}")
            print(f"Time: {post[4]}")

            self.cursor.execute(f"SELECT media_type, file_id FROM media WHERE post_id = {post[0]}")
            media = self.cursor.fetchall()
            if media:
                print(f"Media:")
                for media_item in media:
                    print(f"Type: {media_item[0]}, ID: {media_item[1]}")

            self.cursor.execute(f"SELECT emoji, count FROM reactions WHERE post_id = {post[0]}")
            reactions = self.cursor.fetchall()
            if reactions:
                print("Reactions:")
                for reaction in reactions:
                    print(f"Emoji: {reaction[0]}, Count: {reaction[1]}")

            print("\n")

    def load_data(self):
        try:
            self.cursor.execute("SELECT * FROM channels")
            self.channels = self.cursor.fetchall()

            self.cursor.execute("SELECT * FROM posts")
            self.posts = self.cursor.fetchall()

            self.cursor.execute("SELECT * FROM media")
            self.media = self.cursor.fetchall()

            self.cursor.execute("SELECT * FROM reactions")
            self.reactions = self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def clear_data(self):
        self.cursor.execute("DELETE FROM channels")
        self.cursor.execute("DELETE FROM posts")
        self.cursor.execute("DELETE FROM media")
        self.cursor.execute("DELETE FROM reactions")
        self.conn.commit()

if __name__ == "__main__":
    api_id = int(input("Enter your API id: "))
    api_hash = input("Enter your API hash: ")

    client = TelegramClient(api_id, api_hash)

    while True:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("1. Get data from Telegram channel")
        print("2. Print current data")
        print("3. Save data to backup")
        print("4. Load data from backup")
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
            client.save_data()
        elif choice == 4:
            client.load_data()
        elif choice == 5:
            client.clear_data()
        elif choice == 6:
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
            time.sleep(1)
            continue