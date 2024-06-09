import os
import json

from cluster import clusterizer
from Tokenize import tokenizer, vectorizer
import faiss
import numpy as np
import pandas as pd


class reactions_predicter:
    def __init__(self, posts: pd.DataFrame, reactions_column: str):
        settings_file = open(os.path.dirname(__file__) + "/src/settings.json")
        settings = json.load(settings_file)
        self.reactions = posts[reactions_column]
        self.posts = posts.drop(columns=[reactions_column])
        self.tokenizer = tokenizer.tokenize()
        self.vectorizer = vectorizer.vectorize()
        self.clusterizer = clusterizer.clustering()
        if settings["create_vectors"] == 1:
            tokens_list = posts["post_text"].apply(self.tokenizer.predict_with_set)
            self.vectors = [self.vectorizer.predict(tokens) for tokens in tokens_list]
            self.clusterizer.fit(self.vectors)
            clusters = self.clusterizer.predict(self.vectors)
            self.vectors = np.hstack(
                (np.array(self.vectors), clusters.reshape((-1, 1)))
            )
            np.save("src/vectors", self.vectors)
        else:
            self.vectors = np.load("src/vectors.npy")
        index_filename = settings["index"]["name"]
        self.index = faiss.read_index(
            os.path.dirname(__file__) + "/index/" + index_filename
        )
        self.num_neighbours = settings["index"]["num_neighbours"]

    def predict(self, text):
        text_tokens = self.tokenizer.predict_with_set(text)
        text_vectors = [self.vectorizer.predict(text_tokens)]
        if self.clusterizer.model_type == "Kmeans":
            text_cluster = self.clusterizer.predict(text_vectors)
        else:
            text_cluster = self.clusterizer.predict(
                self.vectors[:, :-1] + text_vectors
            )[-1]

        text_vectors = np.hstack((text_vectors, text_cluster.reshape(1, -1)))
        text_vectors.reshape(1, -1)
        _, indices = self.index.search(text_vectors, self.num_neighbours)
        reactions_percentage_dict = {}

        def fix(dictionary, eps):
            sum = 0
            for key in dictionary:
                sum += dictionary[key]
            to_delete = []
            for key in dictionary:
                dictionary[key] /= sum
                if dictionary[key] < eps:
                    to_delete.append(key)
            for key in to_delete:
                dictionary.pop(key)

        def decode_reaction(reaction):
            reversed_str = reaction[::-1]
            number = ""
            idx = 0
            while idx < len(reversed_str):
                ch = reversed_str[idx]
                if ch.isdigit():
                    number += ch
                else:
                    break
                idx += 1
            number = number[::-1]
            reaction = reaction[:-(idx)]
            return reaction, number

        for post in indices[0]:
            reactions = self.reactions.iloc[post]
            reactions = reactions.split(",")
            total_reactions = 0
            for reaction in reactions:
                reaction, number = decode_reaction(reaction)
                number = int(number)
                total_reactions += number
            for reaction in reactions:
                reaction, number = decode_reaction(reaction)
                number = int(number)
                if reaction not in reactions_percentage_dict:
                    reactions_percentage_dict[reaction] = number / total_reactions
                else:
                    reactions_percentage_dict[reaction] += number / total_reactions
            fix(reactions_percentage_dict, 0)
        return reactions_percentage_dict
