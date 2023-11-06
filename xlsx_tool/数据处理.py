import pandas as pd
import chardet
import numpy as np

input_file = '../表格/845开票-7月-2.xlsx'
output_file = '../表格/845开票-7月-2-最终版2.xlsx'

# 读取CSV文件
df = pd.read_excel(input_file)
df['商品编码'] = df['商品名称'].apply(lambda x: x.split()[0] if pd.notna(x) else None)
df['商品名称'] = df['商品名称'].apply(lambda x: ' '.join(x.split()[1:]) if pd.notna(x) else None)
print(df['商品名称'])
column_names = df.columns.tolist()
df = df[['客户', '供应商', '网超订单号', '商品编码', '商品名称', '订货数量', '销售单价', '销售总价', '采购单价', '采购总价', '结算单价', '结算总价（共享）', '开票时间', '销售发票号', '销售发票备注', '未开票原因', '收款单号', '付款单号', '未付款原因', '备注']]
df.to_excel(output_file, index=False)
