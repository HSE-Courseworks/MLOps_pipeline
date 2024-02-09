import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split

def load_iris_dataset():
    iris = datasets.load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=7)
    return X_train, X_test, y_train, y_test