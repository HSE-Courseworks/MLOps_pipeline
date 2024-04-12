import unittest
from unittest.mock import patch
import requests
from request import url


class TestRequest(unittest.TestCase):
    @patch("requests.get")
    def test_get_request(self, mock_get):
        mock_get.return_value.text = "Test response"
        response = requests.get(url)
        mock_get.assert_called_once_with(url)
        self.assertEqual(response.text, "Test response")

    @patch("requests.post")
    def test_post_request(self, mock_post):
        mock_post.return_value.json.return_value = {"message": "Test message"}
        response = requests.post(url + "/user", json={"name": "TestName"})
        mock_post.assert_called_once_with(url + "/user", json={"name": "TestName"})
        self.assertEqual(response.json()["message"], "Test message")

    @patch("builtins.input", return_value="TestName")
    @patch("requests.post")
    def test_post_request_with_input(self, mock_post, mock_input):
        mock_post.return_value.json.return_value = {"message": "Test message"}
        response = requests.post(url + "/user", json={"name": mock_input()})
        mock_post.assert_called_once_with(url + "/user", json={"name": "TestName"})
        self.assertEqual(response.json()["message"], "Test message")


if __name__ == "__main__":
    unittest.main()
