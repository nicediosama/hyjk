import requests
import urllib.parse
import json
from oceanengine.get_access_token import load_constant
import time

def report_material_get(advertiser_id, fields, timestamp, filtering={"material_type": "video"}, page=1, page_size=10):
    timestamp = min(timestamp / 1000  + 86400 * 3, time.time())
    url = "https://api.oceanengine.com/open_api/v1.0/qianchuan/report/material/get/"
    params = {
        "start_date": time.strftime('%Y-%m-%d', time.gmtime(timestamp)),
        "end_date": time.strftime('%Y-%m-%d', time.gmtime(timestamp)),
        "order_type": "DESC",
        "order_field": "",
        "advertiser_id": advertiser_id,
        "filtering": filtering,
        "fields": fields,
        "page": page,
        "page_size": page_size
    }
    headers = {
    "Access-Token": load_constant()['ACCESSTOKEN']
    }
    # Convert list and dict values to JSON strings
    for key, value in params.items():
        if isinstance(value, (list, dict)):
            params[key] = json.dumps(value)
    # URL encode the parameters
    url_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    # Replace %20 with empty space
    url_params = url_params.replace('%20', '')

    urls = url +'?' + url_params
    return json.loads(requests.request("GET", urls, headers=headers).text)

# advertiser_id=1786505526433801&end_date=2024-08-20&fields=%5B%22ctr%22%2C%22prepay_order_amount%22%5D&filtering=%7B%22material_type%22%3A%22video%22%7D&order_field=&order_type=ASC&page=1&page_size=10&start_date=2024-08-20
# advertiser_id=1786505526433801&end_date=2024-08-20&fields=%5B%22ctr%22%2C%22prepay_order_amount%22%5D&filtering=%7B%22material_type%22%3A%22video%22%7D&order_field=&order_type=ASC&page=1&page_size=10&start_date=2024-08-20


if __name__ == '__main__':
    data_dict = json.loads(report_material_get())
    # print(data_dict)
    # 获取"material_id"的值
    for item in data_dict["data"]["list"]:
        material_id = item["material_id"]
        print(material_id)
