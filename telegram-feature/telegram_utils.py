import pandas as pd
from pyrogram import Client

class TelegramClient:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.app = None

    def connect_to_channel(self):
        self.app = Client('my_account', api_id=self.api_id, api_hash=self.api_hash)

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

if __name__ == "__main__":
    api_id = int(input("Enter your API id: "))
    api_hash = input("Enter your API hash: ")

    client = TelegramClient(api_id, api_hash)
    client.connect_to_channel()

    chat_id = input("Enter chat id: ")
    n = int(input("Enter the number of posts: "))

    channels, posts, media, reactions = client.get_n_last_posts(chat_id, n)

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