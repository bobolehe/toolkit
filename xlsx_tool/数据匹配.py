import pandas as pd
import re
import chardet
import numpy as np

file1 = '..\\w\\11-6\漏洞列表添加验证列数据去重.xlsx'
file2 = '..\\w\\11-6\联通研究院-5台靶标漏洞CVE去重.xlsx'

file1 = pd.read_excel(file1)
file2 = pd.read_excel(file2)

# 选择指定CVE列为空的数据
blank_data1 = file1[~pd.notna(file1['CVE'])]
blank_data2 = file2[~pd.notna(file2['CVE'])]

# 选择指定CVE列不为空的数据
filtered_data1 = file1[pd.notna(file1['CVE'])]
# 选择指定CVE列不为空的数据
filtered_data2 = file2[pd.notna(file2['CVE'])]

# 找到在 filtered_data1 中而不在 filtered_data2 中的数据
data_not_in_filtered_data2 = filtered_data1[~filtered_data1['CVE'].isin(filtered_data2['CVE'])]
d = [data_not_in_filtered_data2, blank_data1]
data_not_in_filtered_data2 = pd.concat(d)
selected_columns = ['漏洞名称', 'CVE', '验证列']  # 指定需要的列
data_not_in_filtered_data2 = data_not_in_filtered_data2[selected_columns]
# 打印或进一步处理这些数据
data_not_in_filtered_data2.to_excel('..\\w\\11-6\漏洞列表单独存在漏洞.xlsx', index=False)

# 连表匹配数据
merged_df = pd.merge(filtered_data1, filtered_data2, left_on='CVE', right_on='CVE', how='outer')
d = [merged_df, blank_data2]
merged_df = pd.concat(d)


def update_source(row):
    if pd.notna(row['漏洞名称_x']) and pd.notna(row['漏洞名称_y']):
        # 如果两列都存在数据，将漏洞来源列的数据在基础上增加 "绿盟"
        return row['漏洞来源'] + ",绿盟"
    elif pd.notna(row['漏洞名称_x']) and not pd.notna(row['漏洞名称_y']):
        # 如果漏洞名称_x不存在但漏洞名称_y存在数据，修改漏洞来源为 "绿盟"
        return "绿盟"
    else:
        # 如果都不存在数据，保持原内容不变
        return row['漏洞来源']


def update_source2(row):
    if not pd.notna(row['漏洞名称_x']):
        if pd.notna(row['漏洞名称_y']):
            # 如果两列都存在数据，将漏洞来源列的数据在基础上增加 "绿盟"
            return row['漏洞名称_y']
        else:
            return row['漏洞名称']
    else:
        return row['漏洞名称_x']


# 使用 apply 方法应用函数来更新"漏洞来源"列
merged_df['漏洞名称_x'] = merged_df.apply(update_source2, axis=1)
merged_df['漏洞来源'] = merged_df.apply(update_source, axis=1)

merged_df['漏洞名称'] = merged_df['漏洞名称_x']
selected_columns = ['漏洞名称', '漏洞来源', 'CVE', '漏洞标签', '验证列']  # 指定需要的列
merged_df = merged_df[selected_columns]
# merged_df.to_excel('..\\w\\11-6\合并数据333.xlsx', index=False)
