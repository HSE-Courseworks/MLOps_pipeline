import json
import os
import numpy as np
from sklearn.cluster import KMeans, HDBSCAN, DBSCAN


class clustering:
    def __init__(self):
        settings_file = open(os.path.dirname(__file__) + "/../src/settings.json")
        settings = json.load(settings_file)
        self.model_type = settings["clusterizer"]["type"]
        if self.model_type == "DBSCAN":
            self.model = DBSCAN()
        elif self.model_type == "HDBSCAN":
            self.model = HDBSCAN()
        elif self.model_type == "KMeans":
            self.model = KMeans(n_clusters=settings["clusterizer"]["kmeans_clusters"])

    def predict(self, vectors):
        if self.model_type == "Kmeans":
            preds = self.model.predict(vectors)
        else:
            preds = self.model.fit_predict(vectors)
        return preds

    def fit(self, vectors):
        if self.model_type == "Kmeans":
            self.model.fit(vectors)
        else:
            pass
