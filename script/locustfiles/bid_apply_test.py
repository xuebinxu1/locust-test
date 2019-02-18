import sys, os


sys.path.append(os.getcwd())
import threading
import time
import random
import hashlib
import json
import utils.oss as oss
import config.constant as constant
import script.credit.image_generator as image_generator
from script.credit.cid_generator import generate
from script.credit.moxie_data import data as moxie_data
from locust import HttpLocust, TaskSequence, task, seq_task

counter = 0

validation_query_param_str = 'companyId={company_id}&channelId={channel_id}&mobile={mobile}&eventId={event_id}'

class WebsiteTasks(TaskSequence):
    def on_start(self):
        # 获取验证码
        company_id = "1"
        channel_id = "0"
        mobile_platform = random.choice([0, 1])
        self.mobile = 13700000000 + self.locust.get_count()

        validation_str = hashlib.md5(str(self.mobile).encode('utf-8')).hexdigest()[3:19]
        header = {"aabbcc": validation_str}
        vcode_req_body = dict(mobile=self.mobile, companyId=company_id, channelId=channel_id,
                              mobilePlatform=mobile_platform)

        self.client.headers.update(header)
        vcode_response = self.client.post('/user/login/vcode', vcode_req_body)
        vcode_response_dict = json.loads(vcode_response.content)

        if vcode_response.status_code != 200:
            vcode_response.failure("get vcode failed")
        else:
            self.vcode = "0123"
            self.event_id = vcode_response_dict['data']['eventId']
            print("get vcode response: ", vcode_response_dict)

        # 登陆
        login_req_body = dict(mobile=self.mobile, companyId=company_id, channelId=channel_id,
                              mobilePlatform=mobile_platform, vcode=self.vcode, eventId=self.event_id)
        login_response = self.client.post('/user/login', login_req_body)
        login_response_dict = json.loads(login_response.content)

        if login_response.status_code != 200:
            login_response.failure("login failed, mobile: ", self.mobile)
        else:
            self.token = login_response_dict['data']['token']
            print("get vcode response: ", login_response_dict)

        # 上传照片
        front_image = image_generator.get_image_bytes('正面')
        back_image = image_generator.get_image_bytes('背面')
        oss.upload_file(str(self.mobile) + 'front', front_image)
        oss.upload_file(str(self.mobile) + 'back', back_image)


    @seq_task(1)
    @task(1)
    def profile(self):
        """
        实名认证
        :return:
        """

        # 获取认证项
        self.get_validation_item()

        profile_response = self.request_profile_validation()
        profile_response_dict = json.loads(profile_response.content)

        print(profile_response_dict)
        if profile_response.status_code == 200:
            if profile_response_dict['code'] == '200' and profile_response_dict['data']['verified']:
                print(str(self.mobile) + "实名认证成功")
        else:
            print(profile_response)
            print(str(self.mobile) + "实名认证失败")
            # self.interrupt()

    @seq_task(2)
    @task(1)
    def carrier(self):
        """
        运营商认证
        :return:
        """
        company_id = "1"
        channel_id = "0"
        header = {"token": self.token}

        print("moxie carrier request")
        # 数据源
        # payload = dict(eventId=self.event_id, result=moxie_data)
        # self.client.post("http://10.10.10.200:20997/rum/test", payload)

        # 回调
        carrier_callback_body = dict(mobile=self.mobile, companyId=company_id, channelId=channel_id, status="1")
        carrier_callback_response = self.client.post('/carrier/callback', carrier_callback_body)
        if carrier_callback_response.status_code != 200:
            print(str(self.mobile) + "运营商认证失败")
        else:
            # 查询运营商状态
            self.client.headers.update(header)
            carrier_status_response = self.client.get('/carrier/status?' + validation_query_param_str
                            .format(company_id=company_id, channel_id=channel_id,
                                    mobile=self.mobile, event_id=self.event_id))
            carrier_response_dict = json.loads(carrier_status_response.content)

            print(carrier_response_dict)
            if carrier_status_response.status_code == 200:
                if carrier_response_dict['code'] == '200' and carrier_response_dict['data']['verified']:
                    print(str(self.mobile) + "运营商认证成功")
            else:
                print(carrier_status_response)
                print(str(self.mobile) + "运营商认证失败")

    @seq_task(3)
    @task(1)
    def bankcard(self):
        """
        银行卡认证
        :return:
        """


        return

    def get_validation_item(self):
        """
        认证项
        :return:
        """
        company_id = "1"
        channel_id = "0"
        header = {"token": self.token}
        validation_url = '/basic/user/validation?' + validation_query_param_str\
            .format(company_id=company_id, channel_id=channel_id, mobile=self.mobile, event_id=self.event_id)

        self.client.headers.update(header)
        validation_response = self.client.get(validation_url)
        validation_response_dict = json.loads(validation_response.content)

        if validation_response.status_code == 200:
            self.validation_item = validation_response_dict['data']
            print("获取认证项成功")
            print(self.validation_item)
        else:
            print("获取认证项失败")
            self.interrupt()

    def request_profile_validation(self):
        company_id = "1"
        channel_id = "0"
        self.name = "某某"
        self.cid = generate()
        education_level = random.randint(0, 3)
        marital_status = random.randint(0, 4)
        income_level = random.randint(0, 6)
        front_img_url = constant.TEST_OSS_URL + '/' + (str(self.mobile) + 'front')
        back_img_url = constant.TEST_OSS_URL + '/' + (str(self.mobile) + 'back')
        living_test_result = random.choice([0, 1])
        emrg_contact_name_a = "某某A"
        emrg_contact_mobile_a = 13700000000
        emrg_contact_name_b = "某某B"
        emrg_contact_mobile_b = 13700000000

        header = {"token": self.token}
        profile_req_body = dict(mobile=self.mobile, companyId=company_id, channelId=channel_id,
                                name=self.name, cid=self.cid, educationLevel=education_level,
                                maritalStatus=marital_status, incomeLevel=income_level, frontImage=front_img_url,
                                backImage=back_img_url, livingTestResult=living_test_result,
                                emrgContactNameA=emrg_contact_name_a, emrgContactMobileA=emrg_contact_mobile_a,
                                emrgContactNameB=emrg_contact_name_b, emrgContactMobileB=emrg_contact_mobile_b,
                                eventId=self.event_id)
        self.client.headers.update(header)
        profile_response = self.client.post('/profile/upload', profile_req_body)
        print("实名认证请求")
        return profile_response


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
