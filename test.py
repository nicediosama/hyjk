from flybook import *
from oceanengine import *


T = Table('https://pvca9kku524.feishu.cn/base/DIixbNfRGapT6nsG7p5czpB4nUe?table=tblYJGg9pzB4Dk6l&view=vewG9lNl0l')
R = Record()

# 定义映射关系
mapping = {
    'first_publish': '首发',
    'high_quality': '优质',
    'low_efficiency': '低效',
    'improvable': '可提升',
}

for i in R.search_records(T.parent_node, T.table)['data']['items']:
    if '创意ID' in i['fields']:
        if i['fields']['视频位置'] == '袋鼠种草（只放后台）':
            # 袋鼠后台数据
            advertiser_id = 1696907115392007
            flag_dy = False
        elif i['fields']['视频位置'] == '袋鼠种草（发布主页）':
            # 袋鼠直播数据
            advertiser_id = 1696907115392007
            flag_dy = True
        elif i['fields']['视频位置'] == '袋鼠直播':
            # 袋鼠直播数据
            advertiser_id = 1696907115392007
            flag_dy = True
        elif i['fields']['视频位置'] == '肌酸种草（只放后台）':
            # 肌酸后台数据
            advertiser_id = 1784598848285699
            flag_dy = False
        elif i['fields']['视频位置'] == '氮泵（后台）':
            advertiser_id = 1788256212620363
            flag_dy = False
        else: continue
        fields=["stat_cost"]
        filtering = {
            "material_type": "video",
            "material_id": [
                int(i['fields']['创意ID'][0]['text'])
            ]
        }


        if '发布日期' in i['fields']:
            res = report_material_get(advertiser_id, fields, i['fields']['发布日期'], filtering)['data']['list']
        else: continue #未发布则下一条

        fields = {}

        if 'stat_cost' in res[0]['fields']:
            stat_cost = res[0]['fields']['stat_cost']
            if stat_cost < 100 and flag_dy == False:
                fields.update({"消耗": "0-100"})
            elif stat_cost < 150 and flag_dy == True:
                fields.update({"消耗": "0-150"})


        if 'analysis_type' in res[0]:
            analysis_type = [mapping[item] if item in mapping else item for item in res[0]['analysis_type']]
            fields.update({"素材标签": analysis_type})

        
        R.update_a_record(fields, T.parent_node, T.table, i['record_id'])
        print(i)
