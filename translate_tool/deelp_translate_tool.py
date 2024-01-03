import random
import time
import json
import requests


deeplAPI = "https://www2.deepl.com/jsonrpc"

headers = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "x-app-os-name": "iOS",
    "x-app-os-version": "16.3.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "x-app-device": "iPhone13,2",
    "User-Agent": "DeepL-iOS/2.9.1 iOS 16.3.0 (iPhone13,2)",
    "x-app-build": "510265",
    "x-app-version": "2.9.1",
    "Connection": "keep-alive",
}


class TooManyRequestsException(Exception):
    "Raised when there is a 429 error"
    def __str__(self):
        return "Error: Too many requests, your IP has been blocked by DeepL temporarily, please don't request it frequently in a short time."


def getICount(translateText) -> int:
    return translateText.count("i")


def getRandomNumber() -> int:
    random.seed(time.time())
    num = random.randint(8300000, 8399998)
    return num * 1000


def getTimestamp(iCount: int) -> int:
    ts = int(time.time() * 1000)

    if iCount == 0:
        return ts

    iCount += 1
    return ts - ts % iCount + iCount


def translate(text, sourceLang="auto", targetLang="zh", numberAlternative=0, printResult=False, proxies=None) -> str:
    """

    :param text: 翻译文本
    :param sourceLang:
    :param targetLang: 目标语言
    :param numberAlternative:
    :param printResult: 是否打印结果
    :param proxies: 代理
    :return:
    """
    iCount = getICount(text)
    id = getRandomNumber()

    numberAlternative = max(min(3, numberAlternative), 0)

    postData = {
        "jsonrpc": "2.0",
        "method": "LMT_handle_texts",
        "id": id,
        "params": {
            "texts": [{
                "text": text,
                # "requestAlternatives": numberAlternative
            }],
            "splitting": "newlines",
            "lang": {
                "source_lang_user_selected": sourceLang,
                "target_lang": targetLang,
            },
            "timestamp": getTimestamp(iCount),
            "commonJobParams": {
                "wasSpoken": False,
                "transcribe_as": "",
            },
        },
    }
    postDataStr = json.dumps(postData, ensure_ascii=False)
    if (id + 5) % 29 == 0 or (id + 3) % 13 == 0:
        postDataStr = postDataStr.replace('"method":"', '"method" : "', -1)
    else:
        postDataStr = postDataStr.replace('"method":"', '"method": "', -1)

    resp = requests.post(url=deeplAPI, data=postDataStr.encode('utf-8'), headers=headers, proxies=proxies)
    respStatusCode = resp.status_code
    print(respStatusCode)
    if respStatusCode == 429:
        raise TooManyRequestsException

    if respStatusCode != 200:
        print("Error", respStatusCode)
        return

    respJson = resp.json()
    print(respJson)
    if numberAlternative <= 1:
        targetText = respJson["result"]["texts"][0]["text"]
        if printResult:
            print(targetText)
        return targetText

    targetTextArray = []
    for item in respJson["result"]["texts"][0]["alternatives"]:
        targetTextArray.append(item["text"])
        if printResult:
            print(item["text"])

    return targetTextArray


# Example Call
# translate("Stacked Queries SQL Injection", printResult=True, proxies={'http': 'http://192.168.60.78:11111'})
for i in range(10):
    try:
        translate(f"Stacked Queries SQL Injection{i}", printResult=True)
    except Exception as e:
        print('IP暂时被封')
