"""
创建窗口提示功能
"""
import time
import tkinter as tk
from pynput.mouse import Controller

# 创建鼠标控制器
mouse = Controller()


class BubblePopup:
    def __init__(self, root, messages):
        self.root = root
        self.message = messages
        self.popup = tk.Toplevel(root)
        self.x_position, self.y_position = mouse.position
        # 自定义外观
        self.popup.configure(bg="lightblue")  # 设置背景颜色
        width = 0
        height = 50
        for k in messages:
            f = f"{k}:{messages[k]}"
            # 创建第一个文本 Label
            i = tk.Label(self.popup, text=f, bg="lightblue", fg="black", relief="solid", borderwidth=0.5, anchor='w')
            i.pack(fill="both", expand=True, padx=10, pady=5)
            width = max(width, i.winfo_reqwidth())
            height += i.winfo_reqheight()

        # 根据消息文本长度调整窗口大小
        width += 50
        self.popup.geometry(f"{width}x{height}+{self.x_position}+{self.y_position}")

        # 创建关闭按钮
        # close_button = tk.Button(self.popup, text="关闭", command=self.hide)
        # close_button.pack()

    def show(self):
        self.popup.deiconify()
        self.root.after(3000, self.hide)

    def hide(self):
        self.popup.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()

    message = {
        '原文': "123456",
        '翻译': "这是一个自定义外观的气泡式提示，窗口会在指定位置显示。"
    }
    # 创建窗口
    popup = BubblePopup(root, message)
    # 自动关闭
    # popup.show()
    # 启动Tkinter主循环
    root.mainloop()
