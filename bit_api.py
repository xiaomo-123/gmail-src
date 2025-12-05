import requests
import json
import time

# 官方文档地址
# https://doc2.bitbrowser.cn/jiekou/ben-di-fu-wu-zhi-nan.html

# 此demo仅作为参考使用，以下使用的指纹参数仅是部分参数，完整参数请参考文档

url = "http://127.0.0.1:54345"
headers = {'Content-Type': 'application/json'}

proxy_config = {
    "proxyMethod": 2,  # 2=自定义代理，3=API提取IP
    "proxyType": "http",  # 代理类型：http/https/socks5
    "host": "us.922s5.net",  # 代理IP
    "port": 6300,  # 代理端口
    "proxyUserName": "10612568jK-zone-custom-sessid-kxosorD3",  # 代理账号（无则留空）
    "proxyPassword": "PelENhew"   # 代理密码（无则留空）
}

def createBrowser():  # 创建或者更新窗口，指纹参数 browserFingerPrint 如没有特定需求，只需要指定下内核即可，如果需要更详细的参数，请参考文档
    json_data = {
        'name': 'google',  # 窗口名称
        'remark': '',  # 备注
        'proxyMethod': 2,  # 代理方式 2自定义 3 提取IP
        # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
        'proxyType': 'noproxy',
        'host': '',  # 代理主机
        'port': '',  # 代理端口
        'proxyUserName': '',  # 代理账号
        'proxyPassword': '',
        "browserFingerPrint": {  # 指纹对象
            'coreVersion': '124'  # 内核版本，注意，win7/win8/winserver 2012 已经不支持112及以上内核了，无法打开
        }
    }

    res = requests.post(f"{url}/browser/update",
                        data=json.dumps(json_data), headers=headers).json()
    browserId = res['data']['id']
    print(browserId)
    return browserId
def update_proxy_for_single_window(window_id):
    """更新单个窗口的代理IP配置"""
    if not window_id:
        return
    
    update_data = {
        "ids": [window_id],  # 单个ID也需传入列表
        "proxyMethod": proxy_config["proxyMethod"],
        "proxyType": proxy_config["proxyType"],
        "host": proxy_config["host"],
        "port": proxy_config["port"],
        "proxyUserName": proxy_config["proxyUserName"],
        "proxyPassword": proxy_config["proxyPassword"]
    }
    
    res = requests.post(
        f"{url}/browser/update/partial",
        data=json.dumps(update_data),
        headers=headers
    ).json()
    
    if res["success"]:
        print(f"窗口 {window_id} 代理更新成功")
    else:
        print(f"窗口 {window_id} 代理更新失败：{res['msg']}")

def updateBrowser():  # 更新窗口，支持批量更新和按需更新，ids 传入数组，单独更新只传一个id即可，只传入需要修改的字段即可，比如修改备注，具体字段请参考文档，browserFingerPrint指纹对象不修改，则无需传入
    json_data = {'ids': ['93672cf112a044f08b653cab691216f0'],
                 'remark': '我是一个备注', 'browserFingerPrint': {}}
    res = requests.post(f"{url}/browser/update/partial",
                        data=json.dumps(json_data), headers=headers).json()
    print(res)


def openBrowser(id):  # 直接指定ID打开窗口，也可以使用 createBrowser 方法返回的ID
    json_data = {"id": f'{id}'}
    res = requests.post(f"{url}/browser/open",
                        data=json.dumps(json_data), headers=headers).json()
    return res

def getBrowserIds():  # 获取窗口ID列表
    json_data = {"page": 0,
        "pageSize": 10}
    res = requests.post(f"{url}/browser/list",
                        data=json.dumps(json_data), headers=headers).json()
    
    if res.get('success') and 'data' in res and 'list' in res['data']:
        browser_list = res['data']['list']
        ids = [browser['id'] for browser in browser_list]
        return ids
    else:
        print("获取窗口列表失败:", res)
        return []
    
def closeBrowser(id):  # 关闭窗口
    json_data = {'id': f'{id}'}
    requests.post(f"{url}/browser/close",
                  data=json.dumps(json_data), headers=headers).json()


def deleteBrowser(id):  # 删除窗口
    json_data = {'id': f'{id}'}
    print(requests.post(f"{url}/browser/delete",
          data=json.dumps(json_data), headers=headers).json())


if __name__ == '__main__':
    browser_id = createBrowser()
    openBrowser(browser_id)

    time.sleep(10)  # 等待10秒自动关闭窗口

    closeBrowser(browser_id)

    time.sleep(10)  # 等待10秒自动删掉窗口

    deleteBrowser(browser_id)
