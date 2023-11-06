"""
图片裁剪工具
打开图片进行窗口展示
窗口中通过鼠标拖动选中裁剪区域进行裁剪
"""
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from img_tool.AnalyzeImages import analyze_images

import pyscreenshot as ImageGrab
import io


class ImageViewer:
    def __init__(self, root):
        self.root = root
        # 创建窗口成为当前活动窗口
        self.root.focus_force()
        self.root.wm_attributes("-topmost", 1)
        self.root.overrideredirect(True)
        self.image_data = None
        self.image = None
        self.original_image = None
        self.photo = None
        self.has_cropped = False
        self.undo_stack = []

        # 初始化drag_data
        self.drag_data = {'x': 0, 'y': 0, 'item': None}
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.button = tk.Button(root, text="保存", command=self.button_clicked, bg='white', relief="flat", width=3, height=1)
        self.undo_button = tk.Button(root, text="撤销", command=self.undo, bg='white', relief="flat", width=3, height=1)
        self.analyze_button = tk.Button(root, text="取字符", command=self.analyzel, bg='white', relief="flat", width=5, height=1)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.root.bind("<Command-z>", self.undo)
        self.root.bind("<Control-z>", self.undo)
        self.root.bind("<Escape>", self.close_window)

    def load_image(self, images_data):
        """
        初始化显示窗口
        :param images_data: 显示图片
        :return:
        """
        self.image_data = images_data
        image_stream = io.BytesIO(images_data)
        self.image = Image.open(image_stream)
        self.original_image = self.image.copy()
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.config(width=self.image.width, height=self.image.height + 30)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        image_width, image_height = self.image.size
        if image_height > 1050:
            self.canvas.create_window(image_width - 31, image_height - 30, anchor=tk.NW, window=self.button)
            self.canvas.create_window(image_width - 76, image_height - 30, anchor=tk.NW, window=self.analyze_button)
        else:
            self.canvas.create_window(image_width - 31, image_height, anchor=tk.NW, window=self.button)
            self.canvas.create_window(image_width - 76, image_height, anchor=tk.NW, window=self.analyze_button)
        self.canvas.pack()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.image.width) // 2
        y = (screen_height - self.image.height) // 2
        self.root.geometry(f"{self.image.width}x{self.image.height + 30}+{x}+{y}")

    def on_press(self, event):
        if self.has_cropped:
            return
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
        self.drag_data['item'] = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red')

    def on_drag(self, event):
        if self.has_cropped:
            return
        x, y = event.x, event.y
        self.canvas.coords(self.drag_data['item'], self.drag_data['x'], self.drag_data['y'], x, y)

    def on_release(self, event):
        if self.has_cropped:
            return
        x, y = event.x, event.y
        self.canvas.coords(self.drag_data['item'], self.drag_data['x'], self.drag_data['y'], x, y)
        self.selection_rect = self.canvas.coords(self.drag_data['item'])
        self.extract_and_display_selected_area()

    def extract_and_display_selected_area(self):
        """
        裁剪图片显示
        :return:
        """
        if self.selection_rect:
            x1, y1, x2, y2 = map(int, self.selection_rect)
            selected_area = self.image.crop((x1, y1, x2, y2))
            self.photo = ImageTk.PhotoImage(selected_area)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.delete(self.drag_data['item'])
            new_width = x2 - x1
            new_height = y2 - y1
            if new_height > 1050:
                self.canvas.create_window(new_width - 31, new_height - 30, anchor=tk.NW, window=self.button)
                self.canvas.create_window(new_width - 62, new_height - 30, anchor=tk.NW, window=self.undo_button)
                self.canvas.create_window(new_width - 107, new_height - 30, anchor=tk.NW, window=self.analyze_button)
            else:
                self.canvas.create_window(new_width - 31, new_height, anchor=tk.NW, window=self.button)
                self.canvas.create_window(new_width - 62, new_height, anchor=tk.NW, window=self.undo_button)
                self.canvas.create_window(new_width - 107, new_height, anchor=tk.NW, window=self.analyze_button)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - new_width) // 2
            y = (screen_height - new_height) // 2
            self.root.geometry(f"{new_width}x{new_height + 30}+{x}+{y}")
            self.root.update_idletasks()
            self.undo_stack.append(self.original_image.copy())
            self.image = selected_area
            self.has_cropped = True

    def undo(self, event=None):
        """
        撤销激活窗口
        :param event:
        :return:
        """
        if self.undo_stack:
            self.image = self.undo_stack.pop()
            self.has_cropped = False
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            # 重新计算窗口位置，确保居中显示
            new_width, new_height = self.image.width, self.image.height
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            if screen_height > 1040:
                self.canvas.create_window(new_width - 31, new_height - 30, anchor=tk.NW, window=self.button)
                self.canvas.create_window(new_width - 76, new_height - 30, anchor=tk.NW, window=self.analyze_button)
            else:
                self.canvas.create_window(new_width - 31, new_height, anchor=tk.NW, window=self.button)
                self.canvas.create_window(new_width - 76, new_height, anchor=tk.NW, window=self.analyze_button)
            x = (screen_width - new_width) // 2
            y = (screen_height - new_height) // 2
            self.root.geometry(f"{self.image.width}x{self.image.height + 30}+{x}+{y}")

    def button_clicked(self):
        """
        保存图片
        :return:
        """
        if self.image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                self.image.save(save_path)
                self.load_image(self.image_data)

    def analyzel(self):
        """
        提取文字
        :return:
        """
        if self.image:
            print(analyze_images(image=self.image))

    def run(self):
        """运行"""
        # self.root.geometry(f"{self.image.width}x{self.image.height}")
        self.root.mainloop()

    def close_window(self, event=None):
        """关闭窗口"""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("截图工具3066")
    with open("static/25.png", "rb") as image_file:
        image_data = image_file.read()

    screenshot = ImageGrab.grab()
    screenshot_data = io.BytesIO()
    screenshot.save(screenshot_data, format="PNG")

    viewer = ImageViewer(root)
    # viewer.load_image(image_data)
    viewer.load_image(screenshot_data.getvalue())
    viewer.run()
