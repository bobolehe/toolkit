import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.146 Safari/537.36'
}
url = 'https://fanyi.baidu.com/sug'
query = input("请输入需要翻译的内容")
data = {
    'kw': query
}
response = requests.post(url=url, headers=headers, data=data)
dic_obj = response.json()
fileName = query + '.json'
fp = open(fileName, 'w', encoding='utf-8')
json.dump(dic_obj, fp=fp, ensure_ascii=False)
print('over')
