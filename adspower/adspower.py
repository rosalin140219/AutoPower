import requests
import json
from loguru import logger


class AdsPowerClient(object):
    #
    def __init__(self, user_id, api_key, url):
        self.user_id = user_id
        self.api_key = api_key
        self.url = url

    def start_browser(self, serial_number):
        payload = {}
        headers = {}
        uri = "/api/v1/browser/start?serial_number=" + serial_number
        response = requests.request("GET", self.url + uri, headers=headers, data=payload)
        resp = json.loads(response.text)
        if resp["code"] == 0:
            data = resp["data"]
            logger.info(f"启动浏览器成功，响应结果:{data}")
            return data
        else:
            msg = resp["msg"]
            logger.error(f"启动浏览器失败，环境ID:{serial_number}, 失败原因:{msg}")

    def close_browser(self, serial_number):
        payload = {}
        headers = {}
        uri = "/api/v1/browser/stop?serial_number=" + serial_number
        response = requests.request("GET", self.url + uri, headers=headers, data=payload)
        resp = json.loads(response.text)
        if resp["code"] == 0:
            logger.info(f"关闭浏览器成功，环境ID:{serial_number}")
        else:
            msg = resp["msg"]
            logger.error(f"关闭浏览器失败，环境ID:{serial_number}, 失败原因:{msg}")
