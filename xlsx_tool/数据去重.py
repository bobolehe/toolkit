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
    try:
        # 读取CSV文件
        df = pd.read_excel(file_input)

        # 创建一个布尔条件，检查指定列是否为空白值
        condition = df[target].isna()

        # 筛选出包含空白值的行
        rows_with_empty_values = df[condition]

        # 对 '漏洞名称' 列进行去重
        df = df.drop_duplicates(subset=target)

        # 合并去重后的数据和包含空白值的行
        merged_df = pd.concat([df, rows_with_empty_values])

        # 将去重后的数据保存回CSV文件
        # 将去重后的数据另存为表格文件（Excel文件）
        merged_df.to_excel(output_file, index=False)
        print("数据已成功处理并保存为:", file_output)
    except Exception as e:
        print("处理数据时出现错误:", str(e))


if __name__ == '__main__':
    # 定义文件路径
    input_file = '..\\最后一次合\漏洞合并名称去重.xlsx'
    output_file = '..\\最后一次合\漏洞合并名称CVE去重.xlsx'
    target_list = 'CVE'
    run(input_file, output_file, target_list)
