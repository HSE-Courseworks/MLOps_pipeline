from pymorphy2 import MorphAnalyzer
import emoji
import re


class tokenize:
    def __init__(self):
        self.morph = MorphAnalyzer()

    def set_text(self, text):
        self.text = text

    def predict(self):
        def remove_emoji(text):
            return emoji.replace_emoji(text)

        def remove_punctuation(word: str):
            return re.sub(r"[.,:;]", "", word)

        def encode_numbers(word: str):
            if word.isnumeric():
                return "I" + str(len(word))
            elif word[1:].isnumeric():  # обработка чисел вида $*
                return word[0] + "I" + str(len(word) - 1)
            else:  # обработка чисел вида *$
                return word[-1] + "I" + str(len(word) - 1)

        self.text = remove_emoji(self.text)
        words = self.text.split()  # разбиваем текст на слова
        res = []
        for word in words:
            if word.isnumeric() or word[1:].isnumeric() or word[:-1].isnumeric():
                word = encode_numbers(word)
                res.append(word)
            else:
                word = remove_punctuation(word)
                p = self.morph.parse(word)[0]
                res.append(p.normal_form)

        return res

    def predict_with_set(self, text):
        self.set_text(text)
        return self.predict()
