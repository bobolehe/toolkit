import requests


def run(p):
    url = 'https://api-free.deepl.com/v2/translate'

    h = {
        'Authorization': 'DeepL-Auth-Key 8b8150e7-e69a-e8ea-53b6-a04083ec8b8d:fx',
        'Content-Type': 'application/json'
    }

    data = {
        "text": [p],
        "target_lang": "ZH"
    }

    r = requests.post(url, headers=h, json=data)
    if r.status_code == 200:
        zh_value = r.json()['translations'][0]['text']
        return {'status': True, 'data': zh_value}
    else:
        return {'status': False, 'data': ""}
    #   zh_value = r['translations']


if __name__ == '__main__':
    print(run('Deserialization of Untrusted Data vulnerability in YITH YITH WooCommerce Product Add-Ons.This issue affects YITH WooCommerce Product Add-Ons: from n/a through 4.3.0.\n\n'))
