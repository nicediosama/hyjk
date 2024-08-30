import requests
import pickle

#!获取access_token值
def get_access_token(auth_code):
    constant = {
    'APPID': 1807814572082236,
    'SECRET': 'e62f8aca97bd769ba7a5d8a93e6408056af3db50',
    'BACKURL': 'https://hyjk.jlqc.com/',
    'AUTH_CODE': auth_code,
    'access_token':'',
    'expires_in': 0,
    'refresh_token':'',
    'refresh_token_expires_in': 0
    }
    url = 'https://ad.oceanengine.com/open_api/oauth2/access_token/'
    data = {
        'app_id': constant['APPID'],
        'secret': constant['SECRET'],
        'grant_type': 'auth_code',
        'auth_code': constant['AUTH_CODE']
    }
    rsp = requests.post(url, data)
    rsp_data = rsp.json()
    constant['access_token'] = rsp_data['data']['access_token']
    constant['refresh_token'] = rsp_data['data']['refresh_token']
    constant['refresh_token_expires_in'] = rsp_data['data']['refresh_token_expires_in']
    constant['expires_in'] = rsp_data['data']['expires_in']
    save_constant(constant)
    return rsp_data
 
 
# 刷新access_token
def refresh_access_token():
    constant = load_constant()
    if(constant['expires_in'] > 0):
        return {'msg': "No need refresh token"}
    elif(constant['refresh_token_expires_in'] < 0):
        return {'msg': "expiration date refresh token"}
    else:
        url = 'https://ad.oceanengine.com/open_api/oauth2/refresh_token/'
        data = {
            'appid': constant['APPID'],
            'secret': constant['SECRET'],
            'grant_type': 'refresh_token',
            'refresh_token': constant['refresh_token'],
        }
        rsp = requests.post(url, data)
        rsp_data = rsp.json()
        constant['access_token'] = rsp_data['data']['access_token']
        constant['refresh_token'] = rsp_data['data']['refresh_token']
        constant['refresh_token_expires_in'] = rsp_data['data']['refresh_token_expires_in']
        constant['expires_in'] = rsp_data['data']['expires_in']
        save_constant(constant)
        return {'msg': "success refresh token"}

def updata_constant():
    pass

def load_constant(): 
    with open('./constant.pickle', 'rb') as file:
        return pickle.load(file)

def save_constant(constant):
    with open('./constant.pickle', 'wb') as file:
        pickle.dump(constant, file)

if __name__ == '__main__':
    
    print(refresh_access_token())
    print(load_constant())