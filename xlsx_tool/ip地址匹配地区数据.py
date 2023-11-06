import pandas as pd

# 读取两个Excel文件
ip_df = pd.read_excel('IP.xlsx')
ip4_df = pd.read_excel('IPv4归属地-API（高精准-公安版）_20231017114728_updated.xlsx')
ip6_df = pd.read_excel('IPV6归属地-API（区县级）_20231017114753_updated.xlsx')

# 使用merge方法连接三个表格
merged_data = ip_df.merge(ip4_df, left_on='目标IP', right_on='IP', how='left')
merged_data = merged_data.merge(ip6_df, left_on='目标IP', right_on='IP', how='left')


# 创建一个新的数据框来存储匹配后的数据
result_data = pd.DataFrame(columns=['排名', '目标IP', '被攻击次数', '地址'])

# 迭代合并后的表格数据
for index, row in merged_data.iterrows():
    target_ip = row['目标IP']
    ip4 = row['IP_x']
    ip6 = row['IP_y']
    # 判断每一个的类型是否有值
    if type(ip4) == str:
        new_row = {'排名': row['排名'], '目标IP': target_ip, '被攻击次数': row['被攻击次数'], '地址': row['地址_x']}
    else:
        new_row = {'排名': row['排名'], '目标IP': target_ip, '被攻击次数': row['被攻击次数'], '地址': row['地址_y']}
    # 向新的数据框中添加数据
    result_data = pd.concat([result_data, pd.DataFrame([new_row])], ignore_index=True)

# 创建一个新的Excel文件并将匹配后的数据保存到其中
with pd.ExcelWriter('matched_ip.xlsx', engine='xlsxwriter') as writer:
    result_data.to_excel(writer, sheet_name='Sheet1', index=False)

print("数据匹配已完成，并保存到新文件 'matched_ip.xlsx' 中。")
