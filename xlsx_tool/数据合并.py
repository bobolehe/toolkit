"""
指定文件路径，指定数据列数据去重
"""

import pandas as pd
import chardet
import numpy as np


def run(file_input, file_output, target):
    """

    :param file_input: str
    :param file_output: str
    :param target: list
    :return:
    """
    # 检测文件编码
    with open(file_input, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']

    try:

        print("数据已成功处理并保存为:", file_output)
    except Exception as e:
        print("处理数据时出现错误:", str(e))


if __name__ == '__main__':
    # 定义文件路径
    input_file1 = 'D:\yun\文档处理\导出\广东移动POC和EXP漏洞.xlsx'
    input_file2 = 'D:\yun\文档处理\导出\广东移动POC和EXP漏洞.xlsx'

    output_file = 'D:\yun\文档处理\合并1\测试漏洞合并.xlsx'

    df1 = pd.read_excel(input_file1)
    df2 = pd.read_excel(input_file2)
    print([df1, df2])
    d = [df1, df2]
    # 合并去重后的数据和包含空白值的行
    merged_df = pd.concat(d)

    # 将去重后的数据保存回CSV文件
    # 将去重后的数据另存为表格文件（Excel文件）
    merged_df.to_excel(output_file, index=False)
