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
from script.credit.cid_generator import generate as cid_generate
from script.credit.bankcard_generator import generate as bankcard_generate
from script.credit.youdun_callback_data import youdun_callback_data
from script.credit.sdk_data import data as sdk_callback_data
from locust import HttpLocust, TaskSequence, task, seq_task
from script.credit.moxie_callback_data import task_headers, bill_headers, report_headers

counter = 0

validation_query_param_str = 'companyId={company_id}&channelId={channel_id}&mobile={mobile}&eventId={event_id}'


class WebsiteTasks(TaskSequence):
    # def on_start(self):
    #     # 获取验证码
    #     company_id = "1"
    #     channel_id = "0"
    #     mobile_platform = random.choice([0, 1])
    #     self.mobile = 13700000060 + self.locust.get_count()
    #
    #     validation_str = hashlib.md5(str(self.mobile).encode('utf-8')).hexdigest()[3:19]
    #     header = {"aabbcc": validation_str}
    #     vcode_req_body = dict(mobile=self.mobile, companyId=company_id, channelId=channel_id,
    #                           mobilePlatform=mobile_platform)
    #
    #     self.client.headers.update(header)
    #     vcode_response = self.client.post('/user/login/vcode', vcode_req_body)
    #     vcode_response_dict = json.loads(vcode_response.content)
    #     print("get vcode response: ", vcode_response_dict)
    #
    #     if vcode_response.status_code != 200 and vcode_response_dict['code'] != '200':
    #         vcode_response.failure("get vcode failed")
    #         self.interrupt()
    #     else:
    #         self.vcode = "0123"
    #         self.event_id = vcode_response_dict['data']['eventId']
    #
    #     # 登陆
    #     login_req_body = dict(mobile=self.mobile, companyId=company_id, channelId=channel_id,
    #                           mobilePlatform=mobile_platform, vcode=self.vcode, eventId=self.event_id)
    #     login_response = self.client.post('/user/login', login_req_body)
    #     login_response_dict = json.loads(login_response.content)
    #
    #     if login_response.status_code != 200:
    #         login_response.failure("login failed, mobile: ", self.mobile)
    #     else:
    #         self.token = login_response_dict['data']['token']
    #         print("get vcode response: ", login_response_dict)
    #
    #     # 上传照片
    #     front_image = image_generator.get_image_bytes('正面')
    #     back_image = image_generator.get_image_bytes('背面')
    #     oss.upload_file(str(self.mobile) + 'front', front_image)
    #     oss.upload_file(str(self.mobile) + 'back', back_image)

    @seq_task(1)
    @task(1)
    def vcode(self):
        # 获取验证码
        company_id = "200"
        channel_id = "0"
        mobile_platform = random.choice([0, 1])
        self.mobile = 13723001000 + self.locust.get_count()

        validation_str = hashlib.md5(str(self.mobile).encode('utf-8')).hexdigest()[3:19]
        header = {"aabbcc": validation_str}
        vcode_req_body = dict(mobile=self.mobile, companyId=company_id, channelId=channel_id,
                              mobilePlatform=mobile_platform)

        self.client.headers.update(header)
        vcode_response = self.client.post('/user/login/vcode', vcode_req_body)
        vcode_response_dict = json.loads(vcode_response.content)
        print("get vcode response: ", vcode_response_dict)

        if vcode_response.status_code != 200 and vcode_response_dict['code'] != '200':
            vcode_response.failure("get vcode failed")
            self.interrupt()
        else:
            self.vcode = "0123"
            self.event_id = vcode_response_dict['data']['eventId']

    @seq_task(2)
    @task(1)
    def login(self):
        # 获取验证码
        company_id = "200"
        channel_id = "0"
        mobile_platform = random.choice([0, 1])
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

    @seq_task(3)
    @task(1)
    def youdun_recognize_callback(self):
        """
        模拟有盾活体检测回调
        :return:
        """
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        data = json.loads(youdun_callback_data)
        event_id = self.event_id
        data['partner_order_id'] = event_id
        sign_time = data['sign_time']
        sign = self.get_md5_sign(data['partner_order_id'], sign_time)
        data['sign'] = sign.upper()
        try:
            response = self.client.post('http://47.98.129.81:20997/rum/test/callback/youdun/recognition',
                                        data=json.dumps(data),
                                        headers=headers)
            response_data = json.loads(response.content)
            print(response_data)
            if response_data['code'] == '1':
                print("有盾活体检测回调成功。event_id: %s" % event_id)
            else:
                print("有盾回调失败。event_id: %s" % event_id)
        except Exception as e:
            print("有盾回调失败。event_id: %s, exception: %s" % (event_id, e))

    @seq_task(4)
    @task(1)
    def profile(self):
        """
        实名认证
        :return:
        """

        # 获取认证项
        self.name = "某某"
        self.cid = cid_generate()

        self.get_validation_item()

        # 有盾回调
        # result = get_youdun_recognization()
        # payload = dict(eventId=self.event_id, result=result)
        # yd_callback_response = self.client.post('http://47.98.129.81:20997/rum/test/youdun/recognize', data=payload)
        # if yd_callback_response.status_code == 200:
        #     print(str(self.mobile) + "有盾回调发送成功")

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

    @seq_task(5)
    @task(1)
    def sdk_callback(self):
        """
        模拟sdk上传数据
        :return:
        """
        event_id = self.event_id
        payload = dict(eventId=event_id, data=sdk_callback_data)
        try:
            response = self.client.post('http://47.98.129.81:20997/rum/test/sdk/saveData', data=payload)
            if response.status_code == 200:
                print("sdk数据上传成功。event_id: %s" % event_id)
        except Exception as e:
            print("sdk上传数据失败，exception: %s" % e)

    @seq_task(6)
    @task(1)
    def moxie_callback(self):
        """
        模拟魔蝎回调
        :return:
        """
        event_id = self.event_id
        from script.credit.moxie_data import callback_data, bill_data, report_data
        bill_data = json.loads(bill_data)
        report_data = json.loads(report_data)
        callback_data = json.loads(callback_data)
        callback_data['mobile'] = self.mobile
        callback_data['bill'] = bill_data
        callback_data['report'] = report_data
        callback_data['event_id'] = event_id
        try:
            bill_response = self.client.post('http://47.98.129.81:20997/rum/test/callback/moxie-carrier/data',
                                             data=json.dumps(callback_data))
            if bill_response.status_code == 201:
                print("魔蝎回调成功.event_id: %s" % event_id)
            else:
                print("魔蝎回调失败.event_id: %s" % event_id)
        except Exception as e:
            print("魔蝎回调失败.event_id: %s" % event_id)

    @seq_task(7)
    @task(1)
    def carrier(self):
        """
        运营商认证
        :return:
        """
        company_id = "200"
        channel_id = "0"
        header = {"token": self.token}

        # sdk上传
        # sdk_upload_data = dict(eventId=self.event_id, data=sdk_data)
        # sdk_response = self.client.post("http://47.98.129.81:20997/rum/test/sdk/saveData", sdk_upload_data)
        # if sdk_response.status_code == 200:
        #     print(str(self.mobile) + "sdk数据发送成功")

        print("moxie carrier request")

        # 查询运营商状态
        for i in range(5):
            self.client.headers.update(header)
            carrier_status_response = self.client.get('/carrier/status?' + validation_query_param_str
                                                      .format(company_id=company_id, channel_id=channel_id,
                                                              mobile=self.mobile, event_id=self.event_id))
            carrier_response_dict = json.loads(carrier_status_response.content)

            print(carrier_response_dict)
            if carrier_status_response.status_code == 200:
                if carrier_response_dict.get('data') is not None and carrier_response_dict['data']['verified']:
                    print(str(self.mobile) + "运营商认证成功")
                    break
            else:
                print(carrier_status_response)
                print(str(self.mobile) + "运营商认证失败")

    @seq_task(8)
    @task(1)
    def add_bankcard(self):
        """
        银行卡认证
        :return:
        """
        company_id = "200"
        channel_id = "0"

        print("bankcard request")
        # 用户银行卡列表
        self.bankcard_list()

        # 生产银行卡号
        bankcard = bankcard_generate()

        # 银行卡归属查询
        ascription_url = '/bankcard/get/ascription?' \
                         + validation_query_param_str.format(company_id=company_id, channel_id=channel_id,
                                                             mobile=self.mobile, event_id=self.event_id, ) \
                         + '&bankAccountNumber={bankcard_account_number}'.format(bankcard_account_number=bankcard)
        bankcard_info_response = self.client.get(ascription_url)
        bankcard_info_response_dict = json.loads(bankcard_info_response.content)
        print(str(self.mobile) + "银行卡归属")
        print(bankcard_info_response_dict)
        bank_code = bankcard_info_response_dict['data']['bankCode']
        bank_name = bankcard_info_response_dict['data']['bankName']

        # 协议支付短信
        bankcard_request_body = dict(companyId=company_id, channelId=channel_id, mobile=self.mobile,
                                     eventId=self.event_id, bankAccountNumber=bankcard, cid=self.cid,
                                     bankAccountName='某某', bankName=bank_name, bankCode=bank_code,
                                     bankMobile=self.mobile, vcode='000000')
        bankcard_sms_response = self.client.post('/bankcard/sms', bankcard_request_body)
        bankcard_sms_response_dict = json.loads(bankcard_sms_response.content)
        print(str(self.mobile) + "协议支付短信")
        print(bankcard_sms_response_dict)
        if bankcard_sms_response_dict['code'] != '200':
            print(str(self.mobile) + "获取协议支付短信失败")
            return

        self.new_bank_account_id = bankcard_sms_response_dict['data']['newBankAccountId']
        self.order_number = bankcard_sms_response_dict['data']['orderNumber']

        # 添加银行卡
        bankcard_request_body['newBankAccountId'] = self.new_bank_account_id
        bankcard_request_body['orderNumber'] = self.order_number

        bankcard_binding_response = self.client.post('/bankcard/add', bankcard_request_body)
        if bankcard_binding_response.status_code == 200:
            print(str(self.mobile) + "添加银行卡{bankcard}成功".format(bankcard=bankcard))
        else:
            print(str(self.mobile) + "添加银行卡{bankcard}失败".format(bankcard=bankcard))

    @seq_task(9)
    @task(1)
    def choose_bankcard(self):
        # 选择银行卡
        company_id = "200"
        channel_id = "0"

        # 用户银行卡列表
        bankcard_response_dict = self.bankcard_list()
        bankcard_list = list(bankcard_response_dict['data'])
        bankcard_account_dict = random.choice(bankcard_list)
        bankcard_account_id = bankcard_account_dict['bankAccountId']
        bankcard = bankcard_account_dict['bankAccountNumber']

        choose_bankcard_request_body = dict(companyId=company_id, channelId=channel_id, mobile=self.mobile,
                                            bankAccountId=bankcard_account_id)
        choose_bankcard_response = self.client.post('/bankcard/choice', choose_bankcard_request_body)
        if choose_bankcard_response.status_code == 200:
            print(str(self.mobile) + "选择银行卡{bankcard}成功".format(bankcard=bankcard))
        else:
            print(str(self.mobile) + "选择银行卡{bankcard}失败".format(bankcard=bankcard))

    @seq_task(10)
    @task(1)
    def bid_application(self):
        company_id = "200"
        channel_id = "0"
        self.version = "1.1.0"

        header = {"token": self.token}
        self.client.headers.update(header)

        # 认证项
        self.get_validation_item()

        # 用户银行卡列表
        bankcard_response_dict = self.bankcard_list()
        self.bankcard = list(filter(lambda x: x.get('isDefault'), bankcard_response_dict['data']))[0]['bankAccountId']

        # 产品列表
        product_list_url = '/product/list?' + validation_query_param_str \
            .format(company_id=company_id, channel_id=channel_id, mobile=self.mobile, event_id=self.event_id)
        product_response = self.client.get(product_list_url)
        product_response_dict = json.loads(product_response.content)
        product_id_list = list(map(lambda x: x.get('productId'), product_response_dict['data']))

        # 进件条件
        apply_condition_url = '/bid/check/apply/condition?' + validation_query_param_str \
            .format(company_id=company_id, channel_id=channel_id, mobile=self.mobile, event_id=self.event_id) + '&version=' + self.version
        apply_condition_response = self.client.get(apply_condition_url)
        if apply_condition_response.status_code == 200:
            print(str(self.mobile) + "允许查看进件详情")
        else:
            print(str(self.mobile) + "不允许查看进件详情")
            print(apply_condition_response.content)

        # 进件申请
        product_id = random.choice(product_id_list)
        bid_apply_req_body = dict(companyId=company_id, channelId=channel_id, mobile=self.mobile, eventId=self.event_id,
                                  bankAccountId=self.bankcard, productId=product_id, raiseAmount=0.00, version=self.version)
        bid_apply_response = self.client.post('/bid/apply', bid_apply_req_body)
        if bid_apply_response.status_code == 200:
            bid_apply_response_dict = json.loads(bid_apply_response.content)
            print(bid_apply_response_dict)
            if bid_apply_response_dict['code'] == '200':
                bid_id = bid_apply_response_dict['data']['bidId']
                print(str(self.mobile) + "申请进件成功" + str(bid_id))

    def get_validation_item(self):
        """
        认证项
        :return:
        """
        company_id = "200"
        channel_id = "0"
        header = {"token": self.token}
        validation_url = '/basic/user/validation?' + validation_query_param_str \
            .format(company_id=company_id, channel_id=channel_id, mobile=self.mobile, event_id=self.event_id)

        self.client.headers.update(header)
        validation_response = self.client.get(validation_url)
        validation_response_dict = json.loads(validation_response.content)

        if validation_response.status_code == 200:
            self.validation_item = validation_response_dict['data']
            print(str(self.mobile) + "获取认证项成功")
            print(self.validation_item)
        else:
            print(str(self.mobile) + "获取认证项失败")
            self.interrupt()

    def request_profile_validation(self):
        company_id = "200"
        channel_id = "0"
        education_level = random.randint(0, 3)
        marital_status = random.randint(0, 4)
        income_level = random.randint(0, 6)
        front_img_url = constant.TEST_OSS_URL + '/' + (str(self.mobile) + 'front')
        back_img_url = constant.TEST_OSS_URL + '/' + (str(self.mobile) + 'back')
        living_test_result = random.choice([0, 1])
        emrg_contact_name_a = "某某A"
        emrg_contact_mobile_a = 13700000001
        emrg_contact_name_b = "某某B"
        emrg_contact_mobile_b = 13700000002
        province = random.choice(['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北',
                                  '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '台湾', '香港', '澳门'])
        city = '市中心'
        address = '宇宙中心'

        header = {"token": self.token}
        profile_req_body = dict(mobile=self.mobile, companyId=company_id, channelId=channel_id,
                                name=self.name, cid=self.cid, educationLevel=education_level,
                                maritalStatus=marital_status, incomeLevel=income_level, frontImage=front_img_url,
                                backImage=back_img_url, livingTestResult=living_test_result,
                                emrgContactNameA=emrg_contact_name_a, emrgContactMobileA=emrg_contact_mobile_a,
                                emrgContactNameB=emrg_contact_name_b, emrgContactMobileB=emrg_contact_mobile_b,
                                province=province, city=city, detailedAddress=address,
                                eventId=self.event_id)
        self.client.headers.update(header)
        profile_response = self.client.post('/profile/upload', profile_req_body)
        print(str(self.mobile) + "实名认证请求")
        return profile_response

    def bankcard_list(self):
        company_id = "200"
        channel_id = "0"
        header = {"token": self.token}
        validation_url = '/bankcard/list?' + validation_query_param_str \
            .format(company_id=company_id, channel_id=channel_id, mobile=self.mobile, event_id=self.event_id)

        self.client.headers.update(header)
        bankcard_list_response = self.client.get(validation_url)
        bankcard_list_response_dict = json.loads(bankcard_list_response.content)
        print(bankcard_list_response_dict)
        return bankcard_list_response_dict

    def get_md5_sign(self, partner_order_id, sign_time):
        from config.constant import YOUDUN_PUBLIC_KEY, YOUDUN_SECURITY_KEY
        sign_str = "pub_key=%s|partner_order_id=%s|sign_time=%s|security_key=%s" \
                   % (YOUDUN_PUBLIC_KEY, partner_order_id, sign_time, YOUDUN_SECURITY_KEY)
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()


class WebUserLocust(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 1000
    max_wait = 3000
    host = constant.ICEWINE_BASE_URL_STAGING

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
