import unittest
from minio import Minio
import io

MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_BUCKET = "test"


class TestMinio(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.minio_client = Minio(
            "localhost:9000",
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False,
        )
        # Убедимся, что тестовый бакет существует
        if not cls.minio_client.bucket_exists(MINIO_BUCKET):
            cls.minio_client.make_bucket(MINIO_BUCKET)

    @classmethod
    def tearDownClass(cls):
        # Удаляем тестовый бакет и все его содержимое после тестов
        objects = cls.minio_client.list_objects(MINIO_BUCKET, recursive=True)
        for obj in objects:
            cls.minio_client.remove_object(MINIO_BUCKET, obj.object_name)
        cls.minio_client.remove_bucket(MINIO_BUCKET)

    def test_1_minio_connection(self):
        # Проверка, что подключение к MinIO успешно
        self.assertIsNotNone(self.minio_client)

    def test_2_bucket_exists(self):
        # Проверка, что бакет существует
        self.assertTrue(self.minio_client.bucket_exists(MINIO_BUCKET))

    def test_3_put_object(self):
        # Загрузка объекта в бакет
        content = b"Hello, world!"
        content_stream = io.BytesIO(content)
        self.minio_client.put_object(
            MINIO_BUCKET, "hello.txt", content_stream, len(content)
        )

        # Проверка, что объект был успешно загружен
        response = self.minio_client.get_object(MINIO_BUCKET, "hello.txt")
        data = response.read()
        self.assertEqual(data, content)

    def test_4_get_object(self):
        # Получение объекта из бакета
        response = self.minio_client.get_object(MINIO_BUCKET, "hello.txt")
        data = response.read()

        # Проверка содержимого объекта
        self.assertEqual(data, b"Hello, world!")


if __name__ == "__main__":
    unittest.main()

