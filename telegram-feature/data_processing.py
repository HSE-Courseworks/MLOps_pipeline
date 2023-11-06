import sqlite3
import nltk
import re
import pymorphy2
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

class DataProcessor:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def get_data(self, table_name):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT post_text FROM {table_name}")
        data = cursor.fetchall()
        return data

    def remove_punctuation(self, data):
        cleaned_data = []
        for row in data:
            cleaned_row = [re.sub(r'[^\w\s]', '', str(item)) for item in row]
            cleaned_data.append(cleaned_row)
        return cleaned_data

    def tokenize_data(self, data):
        tokenized_data = []
        for row in data:
            tokenized_row = [word_tokenize(str(item)) for item in row]
            tokenized_data.append(tokenized_row)
        return tokenized_data

    def to_lower_case(self, data):
        lower_case_data = []
        for row in data:
            lower_case_row = [[word.lower() for word in item] for item in row]
            lower_case_data.append(lower_case_row)
        return lower_case_data

    def remove_stopwords(self, data):
        data_without_stopwords = []
        russian_stopwords = stopwords.words("russian")
        for row in data:
            row_without_stopwords = [[word for word in item if word not in russian_stopwords] for item in row]
            data_without_stopwords.append(row_without_stopwords)
        return data_without_stopwords

    def lemmatize_data(self, data):
        morph = pymorphy2.MorphAnalyzer()
        lemmatized_data = []
        for row in data:
            lemmatized_row = [[morph.parse(word)[0].normal_form for word in item] for item in row]
            lemmatized_data.append(lemmatized_row)
        return lemmatized_data

    def process_data(self, table_name):
        data = self.get_data(table_name)
        cleaned_data = self.remove_punctuation(data)
        tokenized_data = self.tokenize_data(cleaned_data)
        lower_case_data = self.to_lower_case(tokenized_data)
        data_without_stopwords = self.remove_stopwords(lower_case_data)
        lemmatized_data = self.lemmatize_data(data_without_stopwords)
        return lemmatized_data

    def close_connection(self):
        self.conn.close()

if __name__ == '__main__':
    processor = DataProcessor('telegram_data.db')
    data_without_stopwords = processor.process_data('posts')
    print(data_without_stopwords)
    processor.close_connection()