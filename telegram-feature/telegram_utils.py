import pandas as pd
import os
import time
import glob
from pyrogram import Client

class TelegramClient:
    def __init__(self):
        self.app = None

    def connect_to_account(self, api_id, api_hash):
        self.app = Client('my_account', api_id=api_id, api_hash=api_hash)

    def get_n_last_posts(self, chat_id, n):
        with self.app:
            messages = list(self.app.get_chat_history(chat_id, limit=10*n))
            
            channels = pd.DataFrame(columns=['channel_id', 'channel_name'])
            posts = pd.DataFrame(columns=['post_id', 'channel_id', 'post_text', 'views', 'time'])
            media = pd.DataFrame(columns=['media_id', 'post_id', 'media_type', 'file_id'])
            reactions = pd.DataFrame(columns=['reaction_id', 'post_id', 'emoji', 'count'])
            
            i = -1
            media_group = None
            for message in messages:
                if (media_group is None or 
                    message.media_group_id is None or 
                    message.media_group_id != media_group):
                    i += 1
                    if (i == n): break
                    post_text = message.text if message.text is not None else message.caption
                    
                    posts.loc[i] = [i, chat_id, post_text, message.views, message.date]
                    
                    if message.photo is not None:
                        media.loc[len(media)] = [len(media), i, 'photo', message.photo.file_id]
                    elif message.video is not None:
                        media.loc[len(media)] = [len(media), i, 'video', message.video.file_id]
                    
                    if message.reactions is not None:
                        for reaction in message.reactions.reactions:
                            reactions.loc[len(reactions)] = [len(reactions), i, reaction.emoji, reaction.count]
                    
                    media_group = message.media_group_id if message.media_group_id is not None else None
                elif message.media_group_id == media_group and posts.at[i, 'post_text'] is None and message.caption is not None:
                    posts.at[i, 'post_text'] = message.caption
                else:
                    if message.photo is not None:
                        media.loc[len(media)] = [len(media), i, 'photo', message.photo.file_id]
                    elif message.video is not None:
                        media.loc[len(media)] = [len(media), i, 'video', message.video.file_id]
            
            channels.loc[0] = [chat_id, self.app.get_chat(chat_id).title]
            
            return channels, posts, media, reactions
    
    def save_data(self, channels, posts, media, reactions):
        if not os.path.exists('backup'):
            os.makedirs('backup')

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        channels.to_csv(f'backup/channels_{timestamp}.csv', index=False)
        posts.to_csv(f'backup/posts_{timestamp}.csv', index=False)
        media.to_csv(f'backup/media_{timestamp}.csv', index=False)
        reactions.to_csv(f'backup/reactions_{timestamp}.csv', index=False)

    def print_data(self, channels = None, posts = None, media = None, reactions = None):
        for i, post in posts.iloc[::-1].iterrows():
            print(f"Post {len(posts)-i}:")
            print(f"Channel: {channels.loc[channels['channel_id'] == post['channel_id'], 'channel_name'].values[0]}")
            print(f"Text: {post['post_text']}")
            print(f"Views: {post['views']}")
            print(f"Time: {post['time']}")
            
            post_media = media[media['post_id'] == post['post_id']]
            if not post_media.empty:
                print(f"Media:")
                for _, media_item in post_media.iterrows():
                    print(f"Type: {media_item['media_type']}, ID: {media_item['file_id']}")
            
            post_reactions = reactions[reactions['post_id'] == post['post_id']]
            if not post_reactions.empty:
                print("Reactions:")
                for _, reaction in post_reactions.iterrows():
                    print(f"Emoji: {reaction['emoji']}, Count: {reaction['count']}")
            
            print("\n")

    def load_data(self):
        if not os.path.exists('backup'):
            return

        channels_file = max(glob.glob('backup/channels_*.csv'), key=os.path.getctime)
        posts_file = max(glob.glob('backup/posts_*.csv'), key=os.path.getctime)
        media_file = max(glob.glob('backup/media_*.csv'), key=os.path.getctime)
        reactions_file = max(glob.glob('backup/reactions_*.csv'), key=os.path.getctime)

        try:
            channels = pd.read_csv(channels_file)
            posts = pd.read_csv(posts_file)
            media = pd.read_csv(media_file)
            reactions = pd.read_csv(reactions_file)
        except FileNotFoundError:
            print("One or more backup files do not exist")

        return channels, posts, media, reactions

if __name__ == "__main__":
    api_id = int(input("Enter your API id: "))
    api_hash = input("Enter your API hash: ")

    client = TelegramClient()
    client.connect_to_account(api_id, api_hash)

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
            channels, posts, media, reactions = client.get_n_last_posts(chat_id, n)
        elif choice == 2:
            try:
                client.print_data(channels, posts, media, reactions)
            except NameError:
                print("There is no data to print.")
                time.sleep(1)
        elif choice == 3:
            try:
                client.save_data(channels, posts, media, reactions)
            except NameError:
                print("There is no data to save.")
                time.sleep(1)
        elif choice == 4:
            try:
                channels, posts, media, reactions = client.load_data()
            except TypeError:
                print("There is no data to load.")
                time.sleep(1)
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
            time.sleep(1)