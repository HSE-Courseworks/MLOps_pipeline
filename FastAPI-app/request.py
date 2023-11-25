import requests

url = 'http://localhost:8000'

r = requests.get(url)
print(r.text)
print() 

name = input()
r = requests.post(url+'/user', json = {'name': name})
print(r.json()['message'])