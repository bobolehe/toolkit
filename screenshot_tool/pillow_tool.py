import io
import tkinter as tk
from PIL import ImageGrab
from pynput import keyboard
from img_tool.ImageCroppingTool import ImageViewer

initialization = 0


def on_key_release(key):
    if key == keyboard.KeyCode.from_char('p'):
        take_screenshot()


def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot_data = io.BytesIO()
    screenshot.save(screenshot_data, format="PNG")
    show_screenshot(screenshot_data)


def show_screenshot(screenshot_data):
    root = tk.Tk()
    # 在这里实现显示截图的逻辑，可以使用你喜欢的方式，如直接保存到文件或上传到服务器p
    viewer = ImageViewer(root)
    viewer.load_image(screenshot_data.getvalue())
    viewer.run()


if __name__ == "__main__":
    listener = keyboard.Listener(on_release=on_key_release)
    listener.start()
    listener.join()  # 阻塞主线程，使监听器保持运行
