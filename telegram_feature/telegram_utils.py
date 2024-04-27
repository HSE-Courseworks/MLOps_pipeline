from pyrogram import Client
from datetime import datetime, timedelta
from config import SESSION_STRING
import sqlite3
import os
import time


class TelegramClient:
    def __init__(self, api_id, api_hash, session_string):
        self.app = Client(
            "my_account",
            api_id=api_id,
            api_hash=api_hash,
            session_string=session_string,
        )
        self.conn = sqlite3.connect("dags/telegram_feature/database.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS channels
                               (channel_id INTEGER PRIMARY KEY, channel_name TEXT)"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS posts
                               (post_id INTEGER PRIMARY KEY, channel_id INTEGER, post_text TEXT, views INTEGER, time TEXT)"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS media
                               (media_id INTEGER PRIMARY KEY AUTOINCREMENT, post_id INTEGER, media_type TEXT, file_id TEXT)"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS reactions
                               (reaction_id INTEGER PRIMARY KEY AUTOINCREMENT, post_id INTEGER, emoji TEXT, count INTEGER)"""
        )
        self.conn.commit()

    def save_media(self, message, media_id):
        if not os.path.exists("data"):
            os.makedirs("data")

        channel_id = message.chat.id
        date = message.date

        file_id = (
            message.photo.file_id
            if message.photo is not None
            else message.video.file_id
        )
        if os.path.exists(
            os.path.join(
                "data",
                str(channel_id),
                str(date.year),
                str(date.month),
                str(date.day),
                str(media_id),
            )
        ):
            return
        file_path = self.app.download_media(file_id)

        directory = os.path.join(
            "data", str(channel_id), str(date.year), str(date.month), str(date.day)
        )
        os.makedirs(directory, exist_ok=True)

        new_file_path = os.path.join(directory, str(media_id))
        os.rename(file_path, new_file_path)

    def post_exists_in_db(self, post_id):
        with self.conn:
            self.cursor.execute("SELECT  1 FROM posts WHERE post_id = ?", (post_id,))
            return self.cursor.fetchone() is not None

    def get_n_last_posts(self, chat_id, n):
        with self.app:
            messages = list(self.app.get_chat_history(chat_id, limit=10 * n))
            media_group = None
            two_days_ago = datetime.now() - timedelta(days=2)
            for message in messages:
                if message.date < two_days_ago:
                    break
                if not self.post_exists_in_db(message.id):
                    channel_id = message.chat.id
                    channel_name = message.chat.title
                    self.cursor.execute(
                        "INSERT OR IGNORE INTO channels VALUES (?, ?)",
                        (channel_id, channel_name),
                    )
                    if (
                        media_group is None
                        or message.media_group_id is None
                        or message.media_group_id != media_group
                    ):
                        if message.caption is not None or message.text is not None:
                            post_text = (
                                message.text
                                if message.text is not None
                                else message.caption
                            )
                        else:
                            post_text = "None"
                        if post_text is not None:
                            message_id = message.id
                            self.cursor.execute(
                                "UPDATE posts SET views = ? WHERE post_id = ? AND channel_id = ?",
                                (message.views, message_id, channel_id),
                            )
                            if self.cursor.rowcount == 0:
                                self.cursor.execute(
                                    "INSERT INTO posts VALUES (?, ?, ?, ?, ?)",
                                    (
                                        message_id,
                                        channel_id,
                                        post_text,
                                        message.views,
                                        message.date,
                                    ),
                                )
                            media_group = (
                                message.media_group_id
                                if message.media_group_id is not None
                                else None
                            )
                    else:
                        if message.text is not None or message.caption is not None:
                            post_text = (
                                message.text
                                if message.text is not None
                                else message.caption
                            )
                            self.cursor.execute(
                                "UPDATE posts SET post_text = ? WHERE post_id = ? AND channel_id = ?",
                                (post_text, message_id, channel_id),
                            )

                    # if message.photo is not None:
                    #     self.cursor.execute("SELECT 1 FROM media WHERE post_id = ? AND file_id = ?", (message_id, message.photo.file_unique_id))
                    #     if self.cursor.fetchone() is None:
                    #         self.save_media(message, message.photo.file_unique_id)
                    #         self.cursor.execute("INSERT INTO media (post_id, media_type, file_id) VALUES (?, ?, ?)", (message_id, 'photo', message.photo.file_unique_id))
                    # elif message.video is not None:
                    #     self.cursor.execute("SELECT 1 FROM media WHERE post_id = ? AND file_id = ?", (message_id, message.video.file_unique_id))
                    #     if self.cursor.fetchone() is None:
                    #         self.save_media(message, message.video.file_unique_id)
                    #         self.cursor.execute("INSERT INTO media (post_id, media_type, file_id) VALUES (?, ?, ?)", (message_id, 'video', message.video.file_unique_id))
                if message.reactions is not None:
                    self.cursor.execute(
                        "DELETE FROM reactions WHERE post_id = ?", (message.id,)
                    )
                    for reaction in message.reactions.reactions:
                        self.cursor.execute(
                            "INSERT INTO reactions (post_id, emoji, count) VALUES (?, ?, ?)",
                            (message.id, reaction.emoji, reaction.count),
                        )
        self.conn.commit()

    def print_data(self):
        self.cursor.execute("SELECT * FROM posts ORDER BY post_id ASC")
        posts = self.cursor.fetchall()

        for post in posts:
            print(f"Post {post[0]}:")
            self.cursor.execute(
                f"SELECT channel_id FROM channels WHERE channel_id = {post[1]}"
            )
            print(f"Channel: {self.cursor.fetchone()[0]}")
            print(f"Text: {post[2]}")
            print(f"Views: {post[3]}")
            print(f"Time: {post[4]}")

            self.cursor.execute(
                f"SELECT media_type, file_id FROM media WHERE post_id = {post[0]}"
            )
            media = self.cursor.fetchall()
            if media:
                print(f"Media:")
                for media_item in media:
                    print(f"Type: {media_item[0]}, ID: {media_item[1]}")

            self.cursor.execute(
                f"SELECT emoji, count FROM reactions WHERE post_id = {post[0]}"
            )
            reactions = self.cursor.fetchall()
            if reactions:
                print("Reactions:")
                for reaction in reactions:
                    print(f"Emoji: {reaction[0]}, Count: {reaction[1]}")

            print("\n")

    def backup_db(self):
        backup_dir = "telegram_feature/backup"
        backup_file_path = os.path.join(backup_dir, "telegram_data_tmp.db")

        os.makedirs(backup_dir, exist_ok=True)

        backup_conn = sqlite3.connect(backup_file_path)
        with backup_conn:
            self.conn.backup(backup_conn)
        backup_conn.close()

    def restore_db(self):
        backup_dir = "telegram_feature/backup"
        backup_file_path = os.path.join(backup_dir, "telegram_data_tmp.db")

        if not os.path.isfile(backup_file_path):
            print(f"No such file: {backup_file_path}")
            return

        backup_conn = sqlite3.connect(backup_file_path)

        new_conn = sqlite3.connect("database.db")
        with backup_conn:
            backup_conn.backup(new_conn)
        backup_conn.close()
        new_conn.close()

    def clear_data(self):
        self.cursor.execute("DELETE FROM channels")
        self.cursor.execute("DELETE FROM posts")
        self.cursor.execute("DELETE FROM media")
        self.cursor.execute("DELETE FROM reactions")
        self.conn.commit()

        for root, dirs, files in os.walk("data", topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


def read_tg_info():
    with open("dags/telegram_feature/tg_info.txt", "r") as file:
        api_id = int(file.readline().split(": ")[1])
        api_hash = file.readline().split(": ")[1]
    return api_id, api_hash


def read_tg_channels():
    with open("dags/telegram_feature/tg_channels.txt", "r") as file:
        return [line.strip() for line in file]


if __name__ == "__main__":
    api_id, api_hash = read_tg_info()
    session_string = SESSION_STRING

    client = TelegramClient(api_id, api_hash, session_string)

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
            tg_channels = read_tg_channels()
            for chat_id in tg_channels:
                n = 150
                client.get_n_last_posts(chat_id, n)
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
