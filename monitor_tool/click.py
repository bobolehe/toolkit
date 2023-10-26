"""
鼠标双击 词汇翻译操作
"""

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

baidu_translate = BaiduTranslate(auto=True)


def show_message_box(message):
    messagebox.showinfo("翻译结果", message)


def translate_and_show(y_str):
    f_str = baidu_translate.run(p=y_str)
    message = f"原文：{y_str}\n翻译结果：{f_str['data']}"
    root.after(0, show_message_box, message)


def monitor_mouse():
    click_count = 0
    last_click_time = 0
    double_click_interval = 0.3
    previous_clipboard = clipboard.paste()

    def on_click(x, y, button, pressed):
        nonlocal click_count, last_click_time, previous_clipboard

        if button == button.left and not pressed:
            current_time = time.time()
            if current_time - last_click_time <= double_click_interval:
                click_count += 1
            else:
                click_count = 0

            if click_count == 1:
                pyautogui.hotkey('ctrl', 'c')
                current_clipboard = clipboard.paste()

                if current_clipboard != previous_clipboard:
                    # 启动一个新线程来进行翻译
                    translate_thread = threading.Thread(target=translate_and_show, args=(current_clipboard,))
                    translate_thread.start()
                    previous_clipboard = current_clipboard
                click_count = 0

            last_click_time = current_time

    # 创建鼠标事件监听器
    with Listener(on_click=on_click) as listener:
        listener.join()


# 创建并启动鼠标监控线程
mouse_thread = threading.Thread(target=monitor_mouse, daemon=True)
mouse_thread.start()

# 启动Tkinter主循环
root.mainloop()

previous_clipboard = clipboard.paste()