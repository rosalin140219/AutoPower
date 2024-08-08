import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


class YesCaptcha(object):

    def __init__(self, client_key):
        self.client_key = client_key

    def create_task(self, website_url, website_key, task_type) -> str:
        """
        第一步，创建验证码任务
        :param website_url: 目标网站的域名
        :param website_key: 目标网站key
        :param task_type: 任务类型
        :return taskId : string 创建成功的任务ID
        """
        url = "https://api.yescaptcha.com/createTask"
        data = {
            "clientKey": self.client_key,
            "task": {
                "websiteURL": website_url,
                "websiteKey": website_key,
                "type": task_type,
                "isInvisible": False
            }
        }
        try:
            # 发送JSON格式的数据
            result = requests.post(url, json=data, verify=False).json()
            taskId = result.get('taskId')
            if taskId is not None:
                return taskId
            print(result)
        except Exception as e:
            print(e)

    def get_response(self, task_id: str, task_type: str):
        """
        第二步：使用taskId获取response
        :param task_id: string
        :return response: string 识别结果
        """
        # 循环请求识别结果，3秒请求一次
        times = 0
        while times < 120:
            try:
                url = f"https://api.yescaptcha.com/getTaskResult"
                data = {
                    "clientKey": self.client_key,
                    "taskId": task_id
                }
                result = requests.post(url, json=data, verify=False).json()
                solution = result.get('solution', {})
                if solution:
                    if task_type == 'TurnstileTaskProxyless':
                        return solution.get('token')

                    response = solution.get('gRecaptchaResponse')
                    if response:
                        return response
                print(result)
            except Exception as e:
                print(e)
            times += 3
            time.sleep(3)

    def verify_website(self, website_url, response):
        """
        第三步：提交给网站进行验证
        :param website_url: 目标网站地址
        :param response: 验证码
        :return html: string
        """
        # 如果报错：Message: 'geckodriver' executable needs to be in PATH
        # 参考解决：https://www.jianshu.com/p/1d177b266fd2
        # driver = webdriver.Firefox(executable_path=r'C:\Program Files\Mozilla Firefox\geckodriver.exe')
        driver = webdriver.Chrome()
        driver.get(website_url)
        # 每个网站的处理方式不同，但是大概思路是一样的
        # 无外乎拿到验证码识别结果，然后想办法提交
        # JS回调就是提交的一种
        # 以下步骤请先看看官方官网的代码，
        # 理解一下三个步骤
        # 在网页上执行JS，将获得的验证码写入网页
        driver.execute_script(f'document.getElementById("cf-chl-widget-84rco_response").value="{response}"')
        # 执行回调函数，每个网站回调函数并不相同，需要自己找一下
        # 一般为data-callback=xxxx，这个xxxx就是回调函数
        # driver.execute_script(f'onSuccess("{response}")')
        # 点击提交
        driver.find_element(By.ID, "recaptcha-demo-submit").click()
        return driver.page_source


