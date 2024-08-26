from flybook import *
from oceanengine.report_material_get import *
data_dict = report_material_get()
print(data_dict)

table = Table('https://pvca9kku524.feishu.cn/base/DIixbNfRGapT6nsG7p5czpB4nUe?table=tblLxmV6mRr8yz30&view=vewJI9vdRo')
fields = {
    "视频名称": "多行文本内容",
    "创意ID": data_dict,
}
try:
    print(table_id_records(fields, table.parent_node, table.table_id))
except:
    print("error table_id_records")