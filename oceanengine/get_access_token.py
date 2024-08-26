import requests
import pickle

#!获取access_token值
def get_access_token(APP_ID,secret,auth_code):
    url = 'https://ad.oceanengine.com/open_api/oauth2/access_token/'
    data = {
        'app_id': APP_ID,
        'secret': secret,
        'grant_type': 'auth_code',
        'auth_code': auth_code
    }
    rsp = requests.post(url, data)
    rsp_data = rsp.json()
    return rsp_data
 
 
#!刷新access_token
def get_refresh_token(APP_ID,secret,refresh_token):
    url = 'https://ad.oceanengine.com/open_api/oauth2/refresh_token/'
    data = {
        'appid': APP_ID,
        'secret': secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    rsp = requests.post(url, data)
    rsp_data = rsp.json()
    #print(rsp_data)
    return rsp_data


def init_constant():
    constant = {
    'APPID': 1807814572082236,
    'SECRET': 'e62f8aca97bd769ba7a5d8a93e6408056af3db50',
    'BACKURL': 'https://hyjk.jlqc.com/',
    'AUTH_CODE': 'dea432b89cab439a2d7ca898d9a7bd709204c077',
    'ACCESSTOKEN':'',
    'REFRESHTOKEN':''
    }

    tmp = get_access_token(constant['APPID'], constant['SECRET'], constant['AUTH_CODE'])
    constant['ACCESSTOKEN'] = tmp['data']['access_token']
    constant['REFRESHTOKEN'] = tmp['data']['refresh_token']
    print(constant)
    save_constant(constant)

def updata_constant():
    pass

def load_constant():
    with open('./constant.pickle', 'rb') as file:
        return pickle.load(file)

def save_constant(constant):
    with open('./constant.pickle', 'wb') as file:
        pickle.dump(constant, file)





if __name__ == '__main__':
    # init_constant()
    print(load_constant()['ACCESSTOKEN'])
    pass