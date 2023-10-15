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
            data = {}
            i = -1
            media_group = None
            for message in messages:
                if (media_group is None or 
                    message.media_group_id is None or 
                    message.media_group_id != media_group):
                    i += 1
                    if (i == n): break
                    post_text = message.text if message.text is not None else message.caption
                    data[i] = {
                        'Post text': post_text, 
                        'Views': message.views, 
                        'Reactions': [],
                        'Time': message.date,
                        'Media': []
                    }

                    if message.photo is not None:
                        data[i]['Media'].append({'type':'photo', 'id': message.photo.file_id})
                    elif message.video is not None:
                        data[i]['Media'].append({'type':'video', 'id': message.video.file_id})
                    else:
                        data[i]['Media'] = None
                    if message.reactions is not None:
                        for reaction in message.reactions.reactions:
                            data[i]['Reactions'].append({'emoji': reaction.emoji, 'count': reaction.count})
                    
                    media_group = message.media_group_id if message.media_group_id is not None else None
                elif message.media_group_id == media_group and data[i]['Post text'] is None and message.caption is not None:
                    data[i]['Post text'] = message.caption
                else:
                    if message.photo is not None:
                        data[i]['Media'].append({'type':'photo', 'id': message.photo.file_id})
                    elif message.video is not None:
                        data[i]['Media'].append({'type':'video', 'id': message.video.file_id})
                
            return data

if __name__ == "__main__":
    api_id = int(input("Enter your API id: "))
    api_hash = input("Enter your API hash: ")

    client = TelegramClient(api_id, api_hash)
    client.connect_to_channel()

    chat_id = input("Enter chat id: ")
    n = int(input("Enter the number of posts: "))

    posts = client.get_n_last_posts(chat_id, n)

    i = 0
    for post in reversed(posts.values()):
        print(f"Post {i+1}:")
        print(f"Text: {post['Post text']}")
        print(f"Views: {post['Views']}")
        print(f"Time: {post['Time']}")
        print(f"Media:")
        for media in post['Media']:
            print(f"Type: {media['type']}, ID: {media['id']}")
        print("Reactions:")
        for reaction in post['Reactions']:
            print(f"Emoji: {reaction['emoji']}, Count: {reaction['count']}")
        print("\n")
        
        i += 1