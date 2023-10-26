from pynput.mouse import Listener, Controller
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Listener
from tkinter import messagebox
from translate_tool.baidu_translate import BaiduTranslate

import threading
import tkinter as tk
import pyautogui
import clipboard
import time

# 创建一个Tkinter主窗口
root = tk.Tk()
root.withdraw()  # 隐藏主窗口

# 创建鼠标控制器
mouse = Controller()
# 创建键盘控制器
keyboard = KeyboardController()

# 鼠标双击的时间间隔（秒）
double_click_interval = 0.3
# 剪贴板检测的时间间隔（秒）
clipboard_check_interval = 1
# 上一次剪贴板内容
previous_clipboard = clipboard.paste()

baidu_translate = BaiduTranslate(auto=True)


def show_message_box(message):
    tk.messagebox.showinfo("翻译结果", message)


def translate_and_show(y_str):
    f_str = baidu_translate.run(p=y_str)
    message = f"原文：{y_str}\n翻译结果：{f_str['data']}"
    BubblePopup()
    root.after(0, show_message_box, message)


def monitor_mouse():
    click_count = 0
    last_click_time = 0

    def on_click(x, y, button, pressed):
        nonlocal click_count, last_click_time

        if button == button.left and not pressed:
            current_time = time.time()

            if current_time - last_click_time <= double_click_interval:
                click_count += 1
            else:
                click_count = 0

            if click_count == 1:
                pyautogui.hotkey('ctrl', 'c')
                click_count = 0

            last_click_time = current_time

    # 创建鼠标事件监听器
    with Listener(on_click=on_click) as listener:
        listener.join()


def monitor_clipboard():
    global previous_clipboard
    while True:
        current_clipboard = clipboard.paste()
        if current_clipboard != previous_clipboard:
            # 启动一个新线程来进行翻译
            translate_thread = threading.Thread(target=translate_and_show, args=(current_clipboard,))
            translate_thread.start()
            previous_clipboard = current_clipboard
        time.sleep(clipboard_check_interval)


# 创建并启动鼠标监控线程
mouse_thread = threading.Thread(target=monitor_mouse, daemon=True)
mouse_thread.start()

# 创建并启动剪贴板监控线程
clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
clipboard_thread.start()

# 启动Tkinter主循环
root.mainloop()
