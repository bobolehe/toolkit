"""百度智能云接口调用翻译"""
import requests
import json

API_KEY = "Pojcm4ACEcAcGICre8IwMZR9"
SECRET_KEY = "DgtIPiUmhzVokhuOrDeUF448WBqb8I5c"


def main(q):
    url = "https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=" + get_access_token()

    payload = json.dumps({
        "from": "en",
        "to": "zh",
        "q": q
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return json.loads(response.text)['result']['trans_result'][0]['dst']


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    q = 'Format string vulnerability in the search97.cgi CGI script in SCO help http server for Unixware 7 allows remote attackers to execute arbitrary commands via format characters in the queryText parameter.'
    main(q)
