import pandas as pd
import os
import time
import glob
from pyrogram import Client

class TelegramClient:
    def __init__(self, api_id, api_hash):
        self.app = Client('my_account', api_id=api_id, api_hash=api_hash)
        self.channels = pd.DataFrame(columns=['channel_id', 'channel_name'])
        self.posts = pd.DataFrame(columns=['post_id', 'channel_id', 'post_text', 'views', 'time'])
        self.media = pd.DataFrame(columns=['media_id', 'post_id', 'media_type', 'file_id'])
        self.reactions = pd.DataFrame(columns=['reaction_id', 'post_id', 'emoji', 'count'])
        self.media_id_counter = 0
        self.reaction_id_counter = 0

    def get_n_last_posts(self, chat_id, n):
        with self.app:
            messages = list(self.app.get_chat_history(chat_id, limit=10*n))
    
            i = -1
            media_group = None
            for message in messages:
                channel_id = message.chat.id
                channel_name = message.chat.title
                self.channels = pd.concat([self.channels, pd.DataFrame([{'channel_id': channel_id, 'channel_name': channel_name}])], ignore_index=True)
                
                if (media_group is None or 
                    message.media_group_id is None or 
                    message.media_group_id != media_group):
                    i += 1
                    if (i == n): break

                    post_text = message.text if message.text is not None else message.caption
                    post_id = message.id
                    self.posts = pd.concat([self.posts, pd.DataFrame([{'post_id': message.id, 'channel_id': channel_id, 'post_text': post_text, 'views': message.views, 'time': message.date}])], ignore_index=True)
                    
                    if message.photo is not None:
                        self.media = pd.concat([self.media, pd.DataFrame([{'media_id': self.media_id_counter, 'post_id': post_id, 'media_type': 'photo', 'file_id': message.photo.file_id}])], ignore_index=True)
                        self.media_id_counter += 1
                    elif message.video is not None:
                        self.media = pd.concat([self.media, pd.DataFrame([{'media_id': self.media_id_counter, 'post_id': post_id, 'media_type': 'video', 'file_id': message.video.file_id}])], ignore_index=True)
                        self.media_id_counter += 1

                    if message.reactions is not None:
                        for reaction in message.reactions.reactions:
                            self.reactions = pd.concat([self.reactions, pd.DataFrame([{'reaction_id': self.reaction_id_counter, 'post_id': post_id, 'emoji': reaction.emoji, 'count': reaction.count}])], ignore_index=True)
                            self.reaction_id_counter += 1

                    media_group = message.media_group_id if message.media_group_id is not None else None
                elif message.media_group_id == media_group and self.posts.at[i, 'post_text'] is None and message.caption is not None:
                    self.posts.at[i, 'post_text'] = message.caption
                else:
                    if message.photo is not None:
                        self.media = pd.concat([self.media, pd.DataFrame([{'media_id': self.media_id_counter, 'post_id': post_id, 'media_type': 'photo', 'file_id': message.photo.file_id}])], ignore_index=True)
                        self.media_id_counter += 1
                    elif message.video is not None:
                        self.media = pd.concat([self.media, pd.DataFrame([{'media_id': self.media_id_counter, 'post_id': post_id, 'media_type': 'video', 'file_id': message.video.file_id}])], ignore_index=True)
                        self.media_id_counter += 1
            
    
    def save_data(self):
        if not os.path.exists('backup'):
            os.makedirs('backup')

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.channels.to_csv(f'backup/channels_{timestamp}.csv', index=False)
        self.posts.to_csv(f'backup/posts_{timestamp}.csv', index=False)
        self.media.to_csv(f'backup/media_{timestamp}.csv', index=False)
        self.reactions.to_csv(f'backup/reactions_{timestamp}.csv', index=False)

    def print_data(self):
        for i, post in self.posts.iloc[::-1].iterrows():
            print(f"Post {len(self.posts)-i}:")
            print(f"Channel: {self.channels.loc[self.channels['channel_id'] == post['channel_id'], 'channel_name'].values[0]}")
            print(f"Text: {post['post_text']}")
            print(f"Views: {post['views']}")
            print(f"Time: {post['time']}")
            
            post_media = self.media[self.media['post_id'] == post['post_id']]
            if not post_media.empty:
                print(f"Media:")
                for _, media_item in post_media.iterrows():
                    print(f"Type: {media_item['media_type']}, ID: {media_item['file_id']}")
            
            post_reactions = self.reactions[self.reactions['post_id'] == post['post_id']]
            if not post_reactions.empty:
                print("Reactions:")
                for _, reaction in post_reactions.iterrows():
                    print(f"Emoji: {reaction['emoji']}, Count: {reaction['count']}")
            
            print("\n")

    def load_data(self):
        if not os.path.exists('backup'):
            print("Backup folder does not exist")
            time.sleep(1)
            return

        channels_file = max(glob.glob('backup/channels_*.csv'), key=os.path.getctime)
        posts_file = max(glob.glob('backup/posts_*.csv'), key=os.path.getctime)
        media_file = max(glob.glob('backup/media_*.csv'), key=os.path.getctime)
        reactions_file = max(glob.glob('backup/reactions_*.csv'), key=os.path.getctime)

        try:
            self.channels = pd.read_csv(channels_file)
            self.posts = pd.read_csv(posts_file)
            self.media = pd.read_csv(media_file)
            self.reactions = pd.read_csv(reactions_file)
        except FileNotFoundError:
            print("One or more backup files do not exist")
            time.sleep(1)
            return

if __name__ == "__main__":
    api_id = int(input("Enter your API id: "))
    api_hash = input("Enter your API hash: ")

    client = TelegramClient(api_id, api_hash)

    while True:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("1. Get data from Telegram channel")
        print("2. Print current data")
        print("3. Save data to backup")
        print("4. Load data from backup")
        print("5. Exit")
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            chat_id = input("Enter chat id: ")
            n = int(input("Enter the number of posts: "))
            client.get_n_last_posts(chat_id, n)
        elif choice == 2:
            if client.posts.empty:
                print("No data to print.")
                time.sleep(1)
                continue
            else:
                client.print_data()
        elif choice == 3:
            if client.posts.empty:
                print("No data to save.")
                time.sleep(1)
                continue
            else:
                client.save_data()
        elif choice == 4:
            client.load_data()
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
            time.sleep(1)
            continue