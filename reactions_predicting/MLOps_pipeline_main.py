import requests
import json


def make_prediction_request(text):
    url = "http://localhost:8000/predict"
    headers = {"Content-Type": "application/json"}
    data = {"text": text}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {e}"}


def main():
    text_to_predict = input("Введите текст для предсказания: ")
    response = make_prediction_request(text_to_predict)

    if "error" in response:
        print(f'Произошла ошибка: {response["error"]}')
    else:
        print(f"Ответ от сервера: {response}")


if __name__ == "__main__":
    main()
