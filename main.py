import json
import random
import time

from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from adspower import adspower


if __name__ == '__main__':
    # 读取配置文件
    with open('adspower/config.json', 'r') as config:
        config = json.load(config)

    # 读取userId
    userId = config["adsConfig"]["userId"]
    # 当前用户最大的环境数量，AdsPower环境编号是从1开始，直到maxSerialNumber
    maxSerialNumber = config["adsConfig"]["maxSerialNumber"]
    # 生成整数数组
    envArr = list(range(1, maxSerialNumber + 1))
    random.shuffle(envArr)
    # 创建client
    adsPowerClient = adspower.AdsPowerClient(userId, config["adsConfig"]["apiKey"], config["adsConfig"]["url"])
    browser = adsPowerClient.start_browser(str(10))
    wsSelenium = browser["ws"]["selenium"]
    debugPort = browser["debug_port"]
    # 通过websocket链接浏览器
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", wsSelenium)
    # For older ChromeDriver under version 79.0.3945.16
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # For ChromeDriver version 79.0.3945.16 or over
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://artio.faucet.berachain.com/")
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div[1]/div[1]/div[2]/div[2]/div/input').send_keys(
        "0x69d9391e22Ba5a0648A518C3649dB0eA7aD738a2")
    time.sleep(20)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div[1]/div[1]/div[3]/button').click()


