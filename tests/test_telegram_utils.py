import unittest
from unittest.mock import patch, MagicMock
from telegram_feature.telegram_utils import TelegramClient
import psycopg2


class TestTelegramClient(unittest.TestCase):

    @patch("telegram_feature.telegram_utils.psycopg2.connect")
    @patch("telegram_feature.telegram_utils.Client")
    def test_init(self, MockClient, MockConnect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        MockConnect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        api_id = "test_api_id"
        api_hash = "test_api_hash"
        session_string = "test_session_string"

        client = TelegramClient(api_id, api_hash, session_string)

        MockClient.assert_called_once_with(
            "my_account",
            api_id=api_id,
            api_hash=api_hash,
            session_string=session_string,
        )
        MockConnect.assert_called_once_with(
            dbname="airflow",
            user="airflow",
            password="airflow",
            host="postgres_airflow",
        )
        self.assertEqual(client.app, MockClient.return_value)
        self.assertEqual(client.conn, mock_conn)
        self.assertEqual(client.cursor, mock_cursor)
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()

    @patch("telegram_feature.telegram_utils.psycopg2.connect")
    @patch("telegram_feature.telegram_utils.Client")
    def test_create_tables_channels(self, MockClient, MockConnect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        MockConnect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        api_id = "test_api_id"
        api_hash = "test_api_hash"
        session_string = "test_session_string"

        client = TelegramClient(api_id, api_hash, session_string)

        client.create_tables()

        mock_cursor.execute.assert_any_call(
            "CREATE TABLE IF NOT EXISTS channels (channel_id BIGINT PRIMARY KEY, channel_name TEXT)"
        )
        mock_conn.commit.assert_called()

    @patch("telegram_feature.telegram_utils.psycopg2.connect")
    @patch("telegram_feature.telegram_utils.Client")
    def test_create_tables_posts(self, MockClient, MockConnect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        MockConnect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        api_id = "test_api_id"
        api_hash = "test_api_hash"
        session_string = "test_session_string"

        client = TelegramClient(api_id, api_hash, session_string)

        client.create_tables()

        mock_cursor.execute.assert_any_call(
            "CREATE TABLE IF NOT EXISTS posts (post_id BIGINT PRIMARY KEY, channel_id BIGINT, post_text TEXT, views INTEGER, time TIMESTAMP)"
        )
        mock_conn.commit.assert_called()

    @patch("telegram_feature.telegram_utils.psycopg2.connect")
    @patch("telegram_feature.telegram_utils.Client")
    def test_create_tables_media(self, MockClient, MockConnect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        MockConnect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        api_id = "test_api_id"
        api_hash = "test_api_hash"
        session_string = "test_session_string"

        client = TelegramClient(api_id, api_hash, session_string)

        client.create_tables()

        mock_cursor.execute.assert_any_call(
            "CREATE TABLE IF NOT EXISTS media (media_id SERIAL PRIMARY KEY, post_id BIGINT, media_type TEXT, file_id TEXT)"
        )
        mock_conn.commit.assert_called()

    @patch("telegram_feature.telegram_utils.psycopg2.connect")
    @patch("telegram_feature.telegram_utils.Client")
    def test_create_tables_reactions(self, MockClient, MockConnect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        MockConnect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        api_id = "test_api_id"
        api_hash = "test_api_hash"
        session_string = "test_session_string"

        client = TelegramClient(api_id, api_hash, session_string)

        client.create_tables()

        mock_cursor.execute.assert_any_call(
            "CREATE TABLE IF NOT EXISTS reactions (reaction_id SERIAL PRIMARY KEY, post_id BIGINT, emoji TEXT, count INTEGER)"
        )
        mock_conn.commit.assert_called()


if __name__ == "__main__":
    unittest.main()
