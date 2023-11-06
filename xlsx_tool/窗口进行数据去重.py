import tkinter as tk
import os
import pandas as pd
from tkinter import filedialog

# 创建主窗口
root = tk.Tk()
root.title("数据去重")
merged_df = None


# 函数：打开文件选择对话框并展示文件的列名
def open_file_dialog():
    file_path = filedialog.askopenfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        show_column_names(file_path)


# 函数：展示文件的列名，允许用户选择去重列
def show_column_names(file_path):
    df = pd.read_excel(file_path)
    column_names = df.columns.tolist()

    popup = tk.Toplevel(root)
    popup.title("文件列名")
    tk.Label(popup, text="选择去重列名：").pack()
    max_width = 200

    # 函数：当用户选择列名后执行数据去重
    def on_button_click(column_name):
        popup.destroy()
        perform_data_deduplication(column_name, df)

    for column in column_names:
        button = tk.Button(popup, text=column, command=lambda col=column: on_button_click(col))
        button.pack()
        max_width = max(max_width, button.winfo_reqwidth())

    popup.geometry(f"{max_width}x{(len(column_names) + 1) * 30}")


# 函数：执行数据去重，保存合并的数据
def perform_data_deduplication(column_name, df):
    condition = df[column_name].isna()
    rows_with_empty_values = df[condition]
    df = df.drop_duplicates(subset=column_name)
    global merged_df
    merged_df = pd.concat([df, rows_with_empty_values])


# 函数：保存合并后的数据到文件
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if not file_path:
        return
    if merged_df is None:
        return
    merged_df.to_excel(file_path, index=False)


# 添加标签和按钮
label1 = tk.Label(root, text="选择需要进行数据去重的文件")
label1.pack()
open_button = tk.Button(root, text="选择文件", command=open_file_dialog)
open_button.pack()
label2 = tk.Label(root, text="保存去重后的文件")
label2.pack()
save_button = tk.Button(root, text="保存文件", command=save_file)
save_button.pack()

# 设置窗口的大小
root.geometry("250x120")

# 启动Tkinter事件循环
root.mainloop()
