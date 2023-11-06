from PIL import Image
from translate_tool.baidu_translate import BaiduTranslate
import pytesseract
import io

# 指定Tesseract可执行文件的路径
pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract.exe'

translate = BaiduTranslate(auto=False)


def analyze_images(image):
    # 使用Tesseract进行文字识别
    text = pytesseract.image_to_string(image)
    # # 翻译文本
    # return translate.run(p=text)['data']
    return text


if __name__ == '__main__':
    # 打开图片
    image = Image.open('static/25.png')
    # image = io.BytesIO(image)
    print(analyze_images(image))
