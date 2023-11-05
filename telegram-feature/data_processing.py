import sqlite3
import nltk
from nltk.tokenize import word_tokenize

#nltk.download('punkt')

class DataProcessor:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def get_data(self, table_name):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT post_text FROM {table_name}")
        data = cursor.fetchall()
        return data

    def tokenize_data(self, data):
        tokenized_data = []
        for row in data:
            tokenized_row = [word_tokenize(str(item)) for item in row]
            tokenized_data.append(tokenized_row)
        return tokenized_data

    def process_data(self, table_name):
        data = self.get_data(table_name)
        tokenized_data = self.tokenize_data(data)
        return tokenized_data

processor = DataProcessor('telegram_data.db')
tokenized_data = processor.process_data('posts')
print(tokenized_data)