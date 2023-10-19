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
            data = pd.DataFrame(columns=['Post text', 'Views', 'Reactions', 'Time', 'Media'])
            i = -1
            media_group = None
            for message in messages:
                if (media_group is None or 
                    message.media_group_id is None or 
                    message.media_group_id != media_group):
                    i += 1
                    if (i == n): break
                    post_text = message.text if message.text is not None else message.caption
                    data.loc[i] = [post_text, message.views, [], message.date, []]

                    if message.photo is not None:
                        data.at[i, 'Media'].append({'type':'photo', 'id': message.photo.file_id})
                    elif message.video is not None:
                        data.at[i, 'Media'].append({'type':'video', 'id': message.video.file_id})

                    if message.reactions is not None:
                        for reaction in message.reactions.reactions:
                            data.at[i, 'Reactions'].append({'emoji': reaction.emoji, 'count': reaction.count})

                    media_group = message.media_group_id if message.media_group_id is not None else None
                elif message.media_group_id == media_group and data.at[i, 'Post text'] is None and message.caption is not None:
                    data.at[i, 'Post text'] = message.caption
                else:
                    if message.photo is not None:
                        data.at[i, 'Media'].append({'type':'photo', 'id': message.photo.file_id})
                    elif message.video is not None:
                        data.at[i, 'Media'].append({'type':'video', 'id': message.video.file_id})

        return data

if __name__ == "__main__":
    api_id = int(input("Enter your API id: "))
    api_hash = input("Enter your API hash: ")

    client = TelegramClient(api_id, api_hash)
    client.connect_to_channel()

    chat_id = input("Enter chat id: ")
    n = int(input("Enter the number of posts: "))

    posts = client.get_n_last_posts(chat_id, n)

    for i, post in posts.iloc[::-1].iterrows():
        print(f"Post {len(posts)-i}:")
        print(f"Text: {post['Post text']}")
        print(f"Views: {post['Views']}")
        print(f"Time: {post['Time']}")
        if post["Media"]:
            print(f"Media:")
            for media in post['Media']:
                print(f"Type: {media['type']}, ID: {media['id']}")
        print("Reactions:")
        for reaction in post['Reactions']:
            print(f"Emoji: {reaction['emoji']}, Count: {reaction['count']}")
        print("\n")