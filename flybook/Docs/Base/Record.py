import requests
import os, json
from dotenv import load_dotenv, find_dotenv
from flybook.Authenticate_and_Authorize.Get_Access_Token import Get_Access_Token

CREATE_A_RECORD_URI = "/open-apis/bitable/v1/apps/{}/tables/{}/records"
CREATE_RECORDS_URI = "/open-apis/bitable/v1/apps/{}/tables/{}/records/batch_create"
UPDATE_A_RECORD_URI = "/open-apis/bitable/v1/apps/{}/tables/{}/records/{}"
SEARCH_RECORDS_URI = "/open-apis/bitable/v1/apps/{}/tables/{}/records/search"

LIMIT_REQUEST = 5


class Record(object):
    # 从 .env 文件加载环境变量
    load_dotenv(find_dotenv())
    FEISHU_HOST = os.getenv("FEISHU_HOST")



    def __init__(self):
        self.tenant_access_token = Get_Access_Token().tenant_access_token

    def create_a_record(self, fields, app_token, table_id):
        # 新增记录
        for i in range(LIMIT_REQUEST):
            url = "{}{}".format(self.FEISHU_HOST, CREATE_A_RECORD_URI.format(app_token, table_id))
            data = json.dumps({
                "fields": fields
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': "Bearer " + self.tenant_access_token
            }
            response = requests.request("POST", url, headers=headers, data=data)
            if(self._check_error_response(response, i)): break
        return response.json()
    

    def update_a_record(self,  fields, app_token, table_id, record_id):
        # 更新记录
        for i in range(LIMIT_REQUEST):
            url = "{}{}".format(self.FEISHU_HOST, UPDATE_A_RECORD_URI.format(app_token, table_id, record_id))
            data = json.dumps({
                "fields": fields
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': "Bearer " + self.tenant_access_token
            }
            response = requests.request("PUT", url, headers=headers, data=data)
            if(self._check_error_response(response, i)): break
        return response.json()


    def search_records(self, app_token, table_id):
        # 查询记录
        for i in range(LIMIT_REQUEST):
            url = "{}{}".format(self.FEISHU_HOST, SEARCH_RECORDS_URI.format(app_token, table_id))
            data = json.dumps({
                
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': "Bearer " + self.tenant_access_token
            }
            response = requests.request("POST", url, headers=headers, data=data)
            if(self._check_error_response(response, i)): break
        return response.json()


    def delete_a_record(self):
        pass

    def create_records(self, records, app_token, table_id):
        # 新增多条记录
        for i in range(LIMIT_REQUEST):
            url = "{}{}".format(self.FEISHU_HOST, CREATE_RECORDS_URI.format(app_token, table_id))
            data = json.dumps({
                "records": records
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': "Bearer " + self.tenant_access_token
            }
            response = requests.request("POST", url, headers=headers, data=data)
            if(self._check_error_response(response, i)): break
        return response.json()


    def update_records(self):
        pass
    def batch_get_records(self):
        pass
    def delete_records(self):
        pass

    def _check_error_response(self, resp, i=-1):
        if resp.status_code == 200 and resp.json()['code'] == 0:
            return True
        else: 
            response = resp.json()
            self._auto_error_response(resp)
            print("重试次数{}, errcode = {}, msg = {}".format(i+1, response['code'], response['msg']))
            if(i == LIMIT_REQUEST): print("达到重试上限")
            return False
    
    def _auto_error_response(self, resp):
        err_code = resp.json()['code']
        match err_code:
            case 0:
                pass
            case 91402:
                pass
                # 未找到指定云文档。请检查入参中 token 相关参数是否正确。请注意区分当前 token 是 wiki token 还是文档 token
            case 1254043:
                pass
                # record_id 不存在
            case 99991661 | 99991663:
                # code:99991661 请求需要使用 token 认证。请检查请求 Header 参数 Authorization 中是否填了正确的 token。填写格式为 Bearer access_token
                # code:99991663 请求所使用的应用访问凭证（tenant_access_token）无效
                self.tenant_access_token = Get_Access_Token().get_tenant_access_token()
            case _:
                return False
        return True

if __name__ == '__main__':
    R = Record()
    filds = {
		"文本": "123"
	}
    app_token = 'DIixbNfRGapT6nsG7p5czpB4nUe'
    table_id = 'tblLxmV6mRr8yz30'
    print(R.create_a_record(filds, app_token, table_id))