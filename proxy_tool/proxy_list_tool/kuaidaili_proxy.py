import requests

url = 'https://www.kuaidaili.com/free/'
print(requests.get(url).content)