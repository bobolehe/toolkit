import tkinter as tk
import os
import pandas as pd
from tkinter import filedialog

# 创建主窗口
root = tk.Tk()
root.title("文件合并")

# 用于存储选择的文件路径的列表
selected_files = []

# 创建一个标签，说明文件选择功能
select_label = tk.Label(root, text="选择要合并的文件:")
select_label.pack()

# 创建一个列表框，用于显示已选择的文件
file_listbox = tk.Listbox(root, width=40, height=10)
file_listbox.pack()


# 定义一个函数，用于打开文件选择对话框并添加所选择的文件到列表中
def open_file_dialog():
    file_path = filedialog.askopenfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        selected_files.append(file_path)
        # 更新文件列表显示
        file_listbox.delete(0, tk.END)
        for i, file in enumerate(selected_files):
            file_listbox.insert(tk.END, f"文件{i + 1}：{os.path.basename(file)}")


# 创建一个按钮，点击按钮时会触发open_file_dialog函数
open_button = tk.Button(root, text="选择文件", command=open_file_dialog)
open_button.pack()


# 定义一个函数，用于合并选择的文件
def merge_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if not file_path:
        return
    pd_datas = []
    if not selected_files:
        return
    # 打开列表文件
    for file in selected_files:
        df = pd.read_excel(file)
        pd_datas.append(df)
    if not pd_datas:
        return
    # 合并
    merged_df = pd.concat(pd_datas, ignore_index=True)
    merged_df.to_excel(file_path, index=False)


# 创建一个按钮，点击按钮时会触发文件合并函数
merge_button = tk.Button(root, text="文件合并", command=merge_file)
merge_button.pack()

# 启动Tkinter事件循环
root.mainloop()
