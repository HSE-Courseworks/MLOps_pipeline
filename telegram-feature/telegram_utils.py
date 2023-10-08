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
            messages = list(self.app.get_chat_history(chat_id, limit=n))
            for message in reversed(messages):
                print(f"Post text: {message.text}\nViews: {message.views}")
                if message.reactions is not None:
                    for reaction in message.reactions.reactions:
                        print(f"Reaction: {reaction.emoji}\ncount: {reaction.count}\n")

api_id = int(input("Enter your API id: "))
api_hash = input("Enter your API hash: ")

client = TelegramClient(api_id, api_hash)
client.connect_to_channel()

chat_id = input("Enter chat id: ")
n = int(input("Enter the number of posts: "))
posts = client.get_n_last_posts(chat_id, n)