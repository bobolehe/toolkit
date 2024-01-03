import requests
import json


def run(p: str):
    url = "https://api.deeplx.org/translate"

    payload = json.dumps({
        "text": p,
        "source_lang": "auto",
        "target_lang": "ZH"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    i = 5
    while i:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.json()['code'] == 200:
            return {'status': True, 'data': response.json()['data']}
        else:
            i -= 1
    return {'status': False, 'data': '翻译失败'}


if __name__ == '__main__':
    print(run(p="see https://www.libssh.org/files/0.10/"))
