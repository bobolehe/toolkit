import pandas as pd
import re
import chardet
import numpy as np

# 定义文件路径
input_file = '..\\w\\11-6\漏洞列表.xlsx'
output_file = '..\\w\\11-6\漏洞列表添加验证列.xlsx'

pattern = r'CVE-\d{4}-\d{4,7}'  # 正则表达式用于匹配 CVE 编号

df = pd.read_excel(input_file)


# 定义一个函数，检查是否存在"可验证"
def check_verification(text):
    if pd.notna(text) and '可验证' in text:
        return '可验证'
    else:
        return np.nan


df['CVE'] = df['漏洞名称'].apply(lambda x: re.search(pattern, x).group() if pd.notna(x) and re.search(pattern, x) else np.nan)
df['验证列'] = df['漏洞名称'].apply(check_verification)
df.to_excel(output_file, index=False)
