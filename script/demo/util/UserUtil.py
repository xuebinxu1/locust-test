import datetime
import hashlib
import json
import random
import requests

import faker

from config import constant
from script.credit import image_generator
from script.credit.bankcard_generator import generate
from utils import oss

fakerInstance = faker.Faker(locale='zh_CN')


def create_time():
    today = datetime.datetime.today()
    now = datetime.datetime.__format__(today, "%Y-%m-%d %H:%M:%S")
    return now


def check_sex(cid):
    _number = str(cid)[-2]
    if int(_number) % 2 == 0:
        return 0
    else:
        return 1


def create_name_by_cid(cid):
    # 身份证倒数第二位能被2整除为女性，否则为男性
    _number = str(cid)[-2]
    if int(_number) % 2 == 0:
        return fakerInstance.name_male()
    else:
        return fakerInstance.name_female()


def create_marital_status():
    # 0:未婚、1:已婚未育、2:已婚已育、3:离异、4:丧偶
    return random.randint(0, 4)


def create_income_level():
    # 月均收入分类（0:无收入、1:0-1000元、2:1000-3000元、3:3000-5000元、4:5000-10000元、5:10000-20000元、6:20000元以上）
    return random.randint(0, 6)


def create_education_level():
    # 教育程度（0硕士及以上、1本科、2大专、3中专/高中及以下
    return random.randint(0, 3)


start, end = "1970-01-01", "2000-12-30"
days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
birth_days = datetime.datetime.strftime(
    datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days)), "%Y%m%d"
)


# class WebDemo(object):

def vcode(company_id,channel_id):
    mobile = fakerInstance.phone_number()
    print("mobile", mobile)
    mobile_platform = random.choice([0, 1])
    print("mobile_platform", mobile_platform)
    cid = generate()
    print("cid", cid)
    name = create_name_by_cid(cid)
    print("name", name)

    # 获取验证码

    validation_str = hashlib.md5(str(mobile).encode('utf-8')).hexdigest()[3:19]
    header = {"aabbcc": validation_str}
    vcode_req_body = dict(mobile=mobile, companyId=company_id, channelId=channel_id,
                          mobilePlatform=mobile_platform)

    vcode_response = requests.post(url=constant.ICEWINE_BASE_URL_STAGING + '/user/login/vcode', data=vcode_req_body,
                                   headers=header)
    vcode_response_dict = json.loads(vcode_response.content)
    print("get vcode response: ", vcode_response_dict)

    if vcode_response.status_code != 200 and vcode_response_dict['code'] != '200':
        vcode_response.failure("get vcode failed")
        # interrupt()
    else:
        _vcode = "0123"
        event_id = vcode_response_dict['data']['eventId']
        return dict(mobile=mobile, company_id=company_id, channel_id=channel_id, mobile_platform=mobile_platform,
                    event_id=event_id)


def login(mobile, company_id, channel_id, mobile_platform, event_id):
    # 登陆
    login_req_body = dict(mobile=mobile, companyId=company_id, channelId=channel_id,
                          mobilePlatform=mobile_platform, vcode="0123", eventId=event_id)
    login_response = requests.post(url=constant.ICEWINE_BASE_URL_STAGING + '/user/login', data=login_req_body)
    login_response_dict = json.loads(login_response.content)

    if login_response.status_code != 200:
        login_response.failure("login failed, mobile: ", mobile)
    else:
        token = login_response_dict['data']['token']
        print("get vcode response: ", login_response_dict)

    # 上传照片
    print("上传照片开始")
    front_image = image_generator.get_image_bytes('正面')
    back_image = image_generator.get_image_bytes('背面')
    oss.upload_file(str(mobile) + 'front', front_image)
    oss.upload_file(str(mobile) + 'back', back_image)
    print("上传照片结束")
    return token


def carrier(token, company_id, channel_id, mobile, event_id):
    """
    运营商认证
    :return:
    """
    header = {"token": token}

    # sdk上传
    # sdk_upload_data = dict(eventId=event_id, data=sdk_data)
    # sdk_response = client.post("http://47.98.129.81:20997/rum/test/sdk/saveData", sdk_upload_data)
    # if sdk_response.status_code == 200:
    #     print(str(mobile) + "sdk数据发送成功")

    print("moxie carrier request")
    validation_query_param_str = 'companyId={company_id}&channelId={channel_id}&mobile={mobile}&eventId={event_id}'

    # 查询运营商状态
    for i in range(5):
        carrier_status_response = requests.get(
            url=constant.ICEWINE_BASE_URL_STAGING + '/carrier/status?' + validation_query_param_str
                .format(company_id=company_id, channel_id=channel_id,
                        mobile=mobile, event_id=event_id), headers=header)
        print("_company_id", company_id)
        print("_channel_id", channel_id)
        print("_mobile", mobile)
        print("event_id", event_id)
        carrier_response_dict = json.loads(carrier_status_response.content)

        print("carrier_response_dict", carrier_response_dict)
        print("carrier_status_response", carrier_status_response)
        if carrier_status_response.status_code == 200:
            if carrier_response_dict.get('data') is not None and carrier_response_dict['data']['verified']:
                print(str(mobile) + "运营商认证成功")
                break
        else:
            print(carrier_status_response)
            print(str(mobile) + "运营商认证失败")


def bankcard_list(token, company_id, channel_id, mobile, event_id):
    validation_query_param_str = 'companyId={company_id}&channelId={channel_id}&mobile={mobile}&eventId={event_id}'
    header = {"token": token}
    validation_url = '/bankcard/list?' + validation_query_param_str \
        .format(company_id=company_id, channel_id=channel_id, mobile=mobile, event_id=event_id)

    bankcard_list_response = requests.get(url=constant.ICEWINE_BASE_URL_STAGING + validation_url, headers=header)
    bankcard_list_response_dict = json.loads(bankcard_list_response.content)
    print(bankcard_list_response_dict)
    return bankcard_list_response_dict


def register(company_id,channel_id):
    vcode_dict = vcode(company_id,channel_id)
    mobile = vcode_dict.get("mobile")
    event_id = vcode_dict.get("event_id")
    mobile_platform = vcode_dict.get("mobile_platform")
    token = login(mobile, company_id, channel_id, mobile_platform, event_id)
    return dict(mobile=mobile,event_id=event_id)
