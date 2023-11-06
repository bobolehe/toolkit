"""
ip地址分拣
"""

import pandas as pd
import re

# 读取Excel文件
df = pd.read_excel("ip地址.xlsx")

# 定义一个正则表达式模式，以匹配IPv4和IPv6地址
ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b|\b[0-9a-fA-F:]+\b'

# 提取IP地址
ip_v4 = []
ip_v6 = []
for ip_data in df["目标IP"]:
    if "." in ip_data:
        ip_v4.append(ip_data)
        continue
    ip_v6.append(ip_data)

print(len(ip_v4), ip_v4)
print(len(ip_v6), ip_v6)

df4 = pd.DataFrame({"ipv4": ip_v4})
df4.to_excel('ip_v4.xlsx', index=False)

df6 = pd.DataFrame({"ipv6": ip_v6})
df6.to_excel('ip_v6.xlsx', index=False)
