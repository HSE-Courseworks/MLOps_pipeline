import unittest
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os


class TestMLflow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Устанавливаем подключение к MLflow серверу
        mlflow.set_tracking_uri("http://localhost:5000")
        os.environ.update(
            {
                "MLFLOW_TRACKING_URI": "http://localhost:5000",
                "MLFLOW_S3_ENDPOINT_URL": "http://localhost:9000",
                "AWS_ACCESS_KEY_ID": "minioadmin",
                "AWS_SECRET_ACCESS_KEY": "minioadmin",
            }
        )
        # Создаем клиент MLflow
        cls.client = MlflowClient()

    def test_1_mlflow_connection(self):
        # Проверяем, что подключение к MLflow серверу успешно
        self.assertIsNotNone(self.client)

    def test_2_model_training_and_logging(self):
        # Загружаем датасет
        iris = load_iris()
        X_train, TestMLflow.X_test, y_train, TestMLflow.y_test = train_test_split(
            iris.data, iris.target, test_size=0.3, random_state=777
        )
        # Обучаем модель
        model = RandomForestClassifier(n_estimators=10, random_state=777)
        model.fit(X_train, y_train)
        # Сохраняем модель в MLflow
        with mlflow.start_run(run_name="random_forest_model") as run:
            mlflow.log_params({"n_estimators": 10, "random_state": 777})
            mlflow.log_metric(
                "accuracy", accuracy_score(self.y_test, model.predict(self.X_test))
            )
            mlflow.sklearn.log_model(model, "random_forest_model")

        # Получаем ID текущего запуска
        TestMLflow.run_id = run.info.run_id
        # Проверяем, что модель была успешно сохранена
        model_info = self.client.get_run(self.run_id).to_dictionary()["data"]["tags"][
            "mlflow.runName"
        ]
        self.assertEqual(model_info, "random_forest_model")

    def test_3_model_loading_and_prediction(self):
        # Загружаем модель из MLflow
        model_uri = f"runs:/{TestMLflow.run_id}/random_forest_model"
        loaded_model = mlflow.sklearn.load_model(model_uri)
        # Предсказываем на тестовом наборе
        y_pred = loaded_model.predict(TestMLflow.X_test)
        # Проверяем, что модель работает правильно
        accuracy = accuracy_score(TestMLflow.y_test, y_pred)
        self.assertGreater(accuracy, 0.8)


if __name__ == "__main__":
    unittest.main()

