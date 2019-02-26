import sys, os

sys.path.append(os.getcwd())
import threading
import time
import random
import hashlib
import json
import config.constant as constant
# from script.credit.moxie_data import data
# from script.credit.youdun_data import get_youdun_recognization
from locust import HttpLocust, TaskSequence, task, seq_task

counter = 0
validation_query_param_str = 'companyId={company_id}&channelId={channel_id}&mobile={mobile}&eventId={event_id}'


class WebsiteTasks(TaskSequence):
    @seq_task(1)  # 任务执行的顺序
    @task(1)  # 任务执行的比重
    def vcode(self):
        """
        用户获取验证码
        :return:
        """
        print("start send vcode")

        company_id = "1"
        channel_id = "0"
        self.mobile = 13720002000 + self.locust.get_count()
        mobile_platform = random.choice([0, 1])
        validation_str = hashlib.md5(str(self.mobile).encode('utf-8')).hexdigest()[3:19]
        timestamp = int(round(time.time() * 1000))

        header = {"aabbcc":validation_str}
        vcode_req_body = dict(mobile = self.mobile, companyId = company_id, channelId = channel_id,
                              mobilePlatform = mobile_platform)

        self.client.headers.update(header)
        response = self.client.post('/user/login/vcode', vcode_req_body)
        vcode_response_dict = json.loads(response.content)

        if response.status_code != 200:
            response.failure("get vcode failed")
        else:
            self.vcode = "0123"
            self.event_id = vcode_response_dict['data']['eventId']
            print("get vcode response: ", vcode_response_dict)

    @seq_task(2)
    @task(1)
    def register(self):
        """
        用户注册
        :return:
        """
        print("start registration")
        company_id = "1"
        channel_id = "0"
        mobile_platform = random.choice([0, 1])
        register_req_body = dict(mobile=self.mobile, companyId=company_id, channelId=channel_id,
                              mobilePlatform=mobile_platform, vcode=self.vcode, eventId = self.event_id)

        response = self.client.post('/user/register', register_req_body)
        if response.status_code != 200:
            response.failure("register failed")
        else:
            print("registered, mobile is ", self.mobile)

        # print("moxie carrier request")
        #
        # payload = dict(eventId=self.event_id, result=data)
        # self.client.post("/rum/test/", payload)

    # @seq_task(3)
    # @task(1)
    # def login(self):
    #     """
    #     用户登陆
    #     :return:
    #     """
    #     company_id = "1"
    #     channel_id = random.choice([None, "0"])
    #     mobile_platform = "1"
    #     login_req_body = dict(mobile = self.mobile, companyId=company_id, channelId=channel_id,
    #                           mobilePlatform=mobile_platform, vcode=self.vcode, eventId=self.event_id)
    #     response = self.client.post('/user/login', login_req_body)
    #     login_response_dict = json.loads(response.content)
    #
    #     if response.status_code != 200:
    #         response.failure("login failed, mobile: ", self.mobile)
    #     else:
    #         self.token = login_response_dict['data']['token']
    #         print("get vcode response: ", login_response_dict)

    # @seq_task(4)
    # @task(3)
    # def product_list(self):
    #     """
    #     产品列表
    #     :return:
    #     """
    #     # 产品列表
    #     company_id = "1"
    #     channel_id = "0"
    #     product_list_url = '/product/list?' + validation_query_param_str \
    #         .format(company_id=company_id, channel_id=channel_id, mobile=self.mobile, event_id=self.event_id)
    #     product_response = self.client.get(product_list_url)
    #     product_response_dict = json.loads(product_response.content)
    #     print(product_response_dict)

        # result = get_youdun_recognization()
        #
        # payload = dict(eventId=self.event_id, result=result)
        # self.client.post('/youdun/recognize', data=payload)


class WebUserLocust(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 1000
    max_wait = 2000
    host = constant.ICEWINE_BASE_URL_LOCAL

    def get_count(self):
        """
        原子操作,获取计数值
        :return:
        """
        global counter
        threadLock = threading.Lock()
        with threadLock:
            counter += 1

        return counter
