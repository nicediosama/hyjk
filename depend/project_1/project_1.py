import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *
from dotenv import load_dotenv, find_dotenv
from flybook.base.table_base import *
import os
import time
from datetime import datetime
from oceanengine import *
import numpy as np

# 从 .env 文件加载环境变量
load_dotenv(find_dotenv())
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

# 多维表格路径，可选参数filter，page_size默认200条数据
def get_table(T : Table,
    filter={
        'conjunction':'or',
        'field_name': '日期',
        'operator': 'is',
        'value': ["CurrentMonth"]
    }, page_token="", page_size=200):
    # 创建client
    client = lark.Client.builder() \
        .app_id(APP_ID) \
        .app_secret(APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象 默认筛选1个月内数据
    request: SearchAppTableRecordRequest = SearchAppTableRecordRequest.builder() \
        .app_token(T.parent_node) \
        .table_id(T.table) \
        .page_token(page_token) \
        .page_size(page_size) \
        .request_body(SearchAppTableRecordRequestBody.builder()
            .filter(FilterInfo.builder()
                .conjunction(filter['conjunction'])
                .conditions([Condition.builder()
                    .field_name(filter['field_name'])
                    .operator(filter['operator'])
                    .value(filter['value'])
                    .build()
                    ])
                .build())
            .automatic_fields(False)
            .build()) \
        .build()

    # 发起请求
    response: SearchAppTableRecordResponse = client.bitable.v1.app_table_record.search(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_record.search failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    # lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    return response.data



def back_table(RECORDS, T : Table):
    # 创建client
    client = lark.Client.builder() \
        .app_id(APP_ID) \
        .app_secret(APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 拼接更新内容
    records = []
    for i in RECORDS:
        for j in RECORDS[i]:
            if j[4] == "":
                tag = []
            else: tag = j[4]
            records.append(AppTableRecord.builder()
                    .fields({"消耗": str(j[2]),
                             "素材标签": tag,
                             "程序找到的发布时间": int(datetime.fromisoformat(j[3]).timestamp()) * 1000})
                    .record_id(j[1])
                    .build())

    # 构造请求对象
    request: BatchUpdateAppTableRecordRequest = BatchUpdateAppTableRecordRequest.builder() \
        .app_token(T.parent_node) \
        .table_id(T.table) \
        .request_body(BatchUpdateAppTableRecordRequestBody.builder()
            .records(records)
            .build()) \
        .build()

    # 发起请求
    response: BatchUpdateAppTableRecordResponse = client.bitable.v1.app_table_record.batch_update(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_record.batch_update failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    # lark.logger.info(lark.JSON.marshal(response.data, indent=4))

# 千川搜索    flag为是否是后台数据，默认为否 时间默认当前时间，start_date="年-月-日"
def qianchuan(RECORD, advertiser_id, start_date=None, end_date=None, flag=True):


# 配置千川筛选条件    
    fields = [
        "stat_cost"
    ]
    filtering = {
        "material_type": "video",
        "material_id": []
    }
    # 写入需查询的所有ID7
    for i in RECORD:
        filtering["material_id"].append(int(i[0]))
    
    page=1
    data = []
    while True:
        res = report_material_get(advertiser_id, fields, start_date, end_date, filtering, page)
        data = data + res['data']['list']
        if page == res['data']['page_info']['total_page']:
            break
        else: page += 1


    # for i in RECORD:
    #     print(i[0])

    # print("------------------")
    # for i in data:
    #     print(i['material_id'])
    # 定义映射关系
    mapping = {
        'first_publish': '首发',
        'high_quality': '优质',
        'low_efficiency': '低效',
        'improvable': '可提升'
    }

    RECORDS = []
    # 判断ID是否相同
    for i in data:
        for j in RECORD:
            if int(j[0]) == i['material_id']:
                # 非后台小于150，后台小于100
                if flag == True and int(i['fields']['stat_cost']) < 100:
                    stat_cost = "0-100"
                elif flag == False and int(i['fields']['stat_cost']) < 150:
                    stat_cost = "0-150"
                else: stat_cost = ""

                RECORDS.append((j[0], j[1], stat_cost , i['create_data'], [mapping[item] if item in mapping else item for item in i['analysis_type']] if 'analysis_type' in i else ""))
                continue
                
    return RECORDS

# 已弃用
# def do_p2_im_message_receive_v1(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
#     print(f'[ do_p2_im_message_receive_v1 access ], data: {lark.JSON.marshal(data, indent=4)}')
# def do_message_event(data: lark.CustomizedEvent) -> None:
#     print(f'[ do_customized_event access ], type: message, data: {lark.JSON.marshal(data, indent=4)}')
# event_handler = lark.EventDispatcherHandler.builder("im.message.receive_v1", "") \
#     .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
#     .register_p1_customized_event("", do_message_event) \
#     .build()



def main(T : Table = Table('https://pvca9kku524.feishu.cn/base/DIixbNfRGapT6nsG7p5czpB4nUe?table=tblYJGg9pzB4Dk6l&view=vewG9lNl0l')):
    RECORD = {
        'DS_houtai': [],
        'DS_zhuye_live': [],
        'JS_houtai': [],
        'DB_houtai': [],
    }
    
    # TODO 找不到记录怎么办
    # 检索有ID的记录
    page_token = ""
    while True:
        gt = get_table(T, page_token = page_token)
        for i in gt.items:
            if '创意ID' in i.fields:
                if i.fields['视频位置'] == '袋鼠种草（只放后台）':
                    RECORD['DS_houtai'].append((i.fields['创意ID'][0]['text'], i.record_id))
                elif i.fields['视频位置'] == '袋鼠种草（发布主页）' or i.fields['视频位置'] == '袋鼠直播':
                    RECORD['DS_zhuye_live'].append((i.fields['创意ID'][0]['text'], i.record_id))
                elif i.fields['视频位置'] == '肌酸种草（只放后台）':
                    RECORD['JS_houtai'].append((i.fields['创意ID'][0]['text'], i.record_id)) 
                elif i.fields['视频位置'] == '氮泵（后台）':
                    RECORD['DB_houtai'].append((i.fields['创意ID'][0]['text'], i.record_id))

        if not gt.has_more:
            break
        page_token = gt.page_token

    
    # 袋鼠主页和直播数据
    RECORD['DS_zhuye_live'] = qianchuan(RECORD['DS_zhuye_live'], advertiser_id = 1696907115392007, flag=False)
    # 袋鼠后台数据
    RECORD['DS_houtai'] = qianchuan(RECORD['DS_houtai'], advertiser_id = 1696907115392007)
    # 肌酸后台数据
    RECORD['JS_houtai'] = qianchuan(RECORD['JS_houtai'], advertiser_id = 1784598848285699)
    # 氮泵数据
    RECORD['DB_houtai'] = qianchuan(RECORD['DB_houtai'], advertiser_id = 1788256212620363)
    back_table(RECORD, T)

    # 已弃用
    # cli = lark.ws.Client(APP_ID, APP_SECRET,
    #                      event_handler=event_handler,
    #                      log_level=lark.LogLevel.DEBUG)
    # cli.start()


# ('7406619503255748671', 'recumxOROF8eCh', 8.95, '2024-08-24T16:48:14+08:00', ['first_publish', 'high_quality'])
# ('7406619484390473764', 'recumxOROFIBrM', 8.52, '2024-08-24T16:48:28+08:00', ['high_quality'])
# ('7407097021004382262', 'recumxOROFldWG', 22.73, '2024-08-25T23:19:48+08:00', ['high_quality'])

if __name__ == "__main__":
    main()
