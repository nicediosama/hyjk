import requests
import os
from dotenv import load_dotenv, find_dotenv
# const
# 开放接口 URI
GET_TENANT_ACCESS_TOKEN_URI = "/open-apis/auth/v3/tenant_access_token/internal"
GET_APP_ACCESS_TOKEN_URI = "/open-apis/auth/v3/app_access_token/internal"
GET_USER_ACCESS_TOKEN_URI = "/open-apis/authen/v1/oidc/access_token"
GET_REFRESH_USER_ACCESS_TOKEN_URI = "/open-apis/authen/v1/oidc/refresh_access_token"
GET_JSAPI_TICKET_URI = "/open-apis/jssdk/ticket/get"
LIMIT_REQUEST = 5

class Get_Access_Token(object):
    # 从 .env 文件加载环境变量
    load_dotenv(find_dotenv())
    APP_ID = os.getenv("APP_ID")
    APP_SECRET = os.getenv("APP_SECRET")
    FEISHU_HOST = os.getenv("FEISHU_HOST")
    

    def __init__(self, app_id=APP_ID, app_secret=APP_SECRET):
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_access_token = ""
        self.user_access_token = ""
        self.user_refresh_token = ""

    def get_token(self, t):
        match t:
            case 'tenant_access_token':
                return self.tenant_access_token
            case 'user_access_token':
                return self.user_access_token
            case _:
                return "error get token"

    def get_tenant_access_token(self):
        # 获取tenant_access_token并保存，参考文档：https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3/auth/tenant_access_token_internal
        url = "{}{}".format(self.FEISHU_HOST, GET_TENANT_ACCESS_TOKEN_URI)
        data = {"app_id": self.app_id, "app_secret": self.app_secret}
        response = requests.post(url, data)
        self._check_error_response(response)
        self.tenant_access_token = response.json()["tenant_access_token"]
        return response.json()["tenant_access_token"]
    

    def get_app_access_token(self):
        # 获取app_access_token
        for i in range(LIMIT_REQUEST):
            url = "{}{}".format(self.FEISHU_HOST, GET_APP_ACCESS_TOKEN_URI)
            data = {"app_id": self.app_id, "app_secret": self.app_secret}
            response = requests.post(url, data)
            if(self._check_error_response(response, i)): break
        return response.json()["app_access_token"]
    
    def get_user_access_token(self, code):
        #TODO
        # 获取user_access_token
        # url = "{}{}".format(self.FEISHU_HOST, USER_ACCESS_TOKEN_URI)
        # data = {"grant_type": "authorization_code", "code": code}
        # response = requests.post(url, data)
        # self._check_error_response(response)
        # return response.json()
        pass

    def refresh_user_access_token(self):
        #TODO
        # 刷新user_access_token
        # url = "{}{}".format(self.FEISHU_HOST, REFRESH_USER_ACCESS_TOKEN_URI)
        # data = {"grant_type": "authorization_code", "refresh_token": pass}
        # response = requests.post(url, data)
        # self._check_error_response(response)
        # return response.json()
        pass

    def get_app_ticket(self):
        # 应用商店应用自动订阅此事件；企业自建应用不需要此事件。
        pass

    def get_jsapi_ticket(self):
        # 获取JSPI临时授权凭证
        for i in range(LIMIT_REQUEST):
            url = "{}{}".format(self.FEISHU_HOST, GET_JSAPI_TICKET_URI)
            headers = {
                "Authorization": "Bearer " + self.tenant_access_token,
                "Content-Type": "application/json",
            }
            response = requests.post(url=url, headers=headers)
            if(self._check_error_response(response, i)): break
        return response.json()["data"]['ticket']

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
            case 99991661 | 99991663:
                # code:99991661 请求需要使用 token 认证。请检查请求 Header 参数 Authorization 中是否填了正确的 token。填写格式为 Bearer access_token
                # code:99991663 请求所使用的应用访问凭证（tenant_access_token）无效
                self.tenant_access_token = self.get_tenant_access_token()
            case _:
                return False
        return True
            



class FeishuException(Exception):
    # 处理并展示飞书侧返回的错误码和错误信息
    def __init__(self, code=0, msg=None):
        self.code = code
        self.msg = msg
    def __str__(self) -> str:
        return "{}:{}".format(self.code, self.msg)
    __repr__ = __str__

if __name__ == '__main__':
    GAT = Get_Access_Token()
    print(GAT.get_tenant_access_token())
