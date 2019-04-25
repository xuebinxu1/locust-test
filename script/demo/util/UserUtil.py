import datetime
import hashlib
import json
import random
import time

import faker
import requests

from config import constant
from script.credit import image_generator
from script.credit.cid_generator import generate as cid_generate
from utils import oss, convert, models
from utils.models import User, UserDetail
from utils.my_snowflake import my_snow

fakerInstance = faker.Faker(locale='zh_CN')

validation_query_param_str = 'companyId={company_id}&channelId={channel_id}&mobile={mobile}&eventId={event_id}'


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


def split_address(address):
    # 根据地址提取省市县
    _province = None
    _city = None
    if address.strip() == '':
        return None
    else:
        address_find_s_index = address.find("省")
        if address_find_s_index == -1:
            address_find_q_index = address.find("区")
            if address_find_q_index == -1:
                address_find_shi_index = address.find("市")
                if address_find_shi_index != -1:
                    _city = address[:address_find_shi_index]
            else:
                address_find_shi_index = address.find("市")
                if address_find_shi_index != -1:
                    _city = address[address_find_q_index + 1:address_find_shi_index]
        else:
            _province = address[:address_find_s_index]
            address_find_shi_index = address.find("市")
            if address_find_shi_index != -1:
                _city = address[address_find_s_index + 1:address_find_shi_index]

    return dict(province=_province, city=_city)


def create_birthday():
    start, end = "1970-01-01", "2000-12-30"
    days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
    birth_day = datetime.datetime.strftime(
        datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days)), "%Y%m%d")
    return birth_day


def vcode(company_id, channel_id):
    mobile = fakerInstance.phone_number()
    print("mobile", mobile)
    mobile_platform = random.choice([0, 1])
    print("mobile_platform", mobile_platform)
    cid = cid_generate()
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
        front_image = image_generator.get_image_bytes('正面')
        back_image = image_generator.get_image_bytes('背面')
        oss.upload_file(str(mobile) + 'front', front_image)
        oss.upload_file(str(mobile) + 'back', back_image)

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
    header = {"token": token}
    validation_url = '/bankcard/list?' + validation_query_param_str \
        .format(company_id=company_id, channel_id=channel_id, mobile=mobile, event_id=event_id)

    bankcard_list_response = requests.get(url=constant.ICEWINE_BASE_URL_STAGING + validation_url, headers=header)
    bankcard_list_response_dict = json.loads(bankcard_list_response.content)
    print(bankcard_list_response_dict)
    return bankcard_list_response_dict


def bid_application_insert(company_id, channel_id, mobile, bankAccountId, productId, raiseAmount, event_id):
    """
    模拟申请进件
    """
    # 查询用户的绑定的卡

    _version = "1.1.0"
    bid = models.Bid()
    bid.bank_account_number


def register(company_id, channel_id):
    """
    请求icewine接口用户注册
    """
    vcode_dict = vcode(company_id, channel_id)
    mobile = vcode_dict.get("mobile")
    event_id = vcode_dict.get("event_id")
    mobile_platform = vcode_dict.get("mobile_platform")
    token = login(mobile, company_id, channel_id, mobile_platform, event_id)

    print("register mobile:", mobile)
    print("register event_id:", event_id)
    print("register mobile_platform:", mobile_platform)
    print("register token:", token)

    return dict(mobile=mobile, event_id=event_id, token=token)


def register_insert(company_id, channel_id, gmt_create, mobile_platform):
    """
    @:param mobile_platform : 所属客户端0:ios, 1:android 2 api
    直接插库进行模拟用户注册
    """
    # 创建user
    # 查询渠道
    channel = convert.query(models.Channel, id=channel_id).one()
    user_cid = cid_generate()
    user_mobile = fakerInstance.phone_number()
    user_id = my_snow().get_next_id()
    user_name = create_name_by_cid(user_cid)
    user_password = hashlib.md5(str(user_mobile).encode('utf-8')).hexdigest()[3:19]
    user_detail_address = fakerInstance.address()
    user_channel_name = channel.name

    print("register_insert user_cid", user_cid)
    print("register_insert user_mobile", user_mobile)
    print("register_insert user_id", user_id)

    user = User()
    user.gmt_create = gmt_create
    user.gmt_modified = gmt_create
    user.is_deleted = 0
    user.id = user_id
    user.company_id = company_id
    user.cid = user_cid
    user.mobile = user_mobile
    user.name = user_name
    user.password = user_password
    user.register_channel = user_channel_name
    user.register_channel_id = channel_id
    user.mobile_md5 = hashlib.md5(str(user_mobile).encode('utf-8')).hexdigest()[3:19]
    convert.add_one(user)

    # 创建user_detail
    user_detail = UserDetail()
    user_detail.id = my_snow().get_next_id()
    user_detail.gmt_create = gmt_create
    user_detail.gmt_modified = gmt_create
    user_detail.is_deleted = 0
    user_detail.cert_item = None
    user_detail.user_id = user_id
    user_detail.company_id = company_id
    user_detail.cid = user_cid
    user_detail.mobile = user_mobile
    user_detail.name = user_name
    user_detail.password = user_password
    user_detail.channel_id = channel_id
    user_detail.channel_name = user_channel_name
    user_detail.province = split_address(user_detail_address).get("province")
    user_detail.city = split_address(user_detail_address).get("city")
    user_detail.address = user_detail_address
    user_detail.gender = check_sex(user_cid)
    user_detail.nationality = "汉"
    user_detail.birthday = create_birthday
    user_detail.marital_status = None
    user_detail.income_level = None
    user_detail.education_level = None
    user_detail.bank_account_id = None
    user_detail.category = None
    user_detail.mobile_platform = mobile_platform
    user_detail.operator_id = None
    user_detail.first_apply_time = gmt_create
    user_detail.first_deduct_time = None
    user_detail.loan_amount = None
    user_detail.raise_amount = None
    user_detail.emrg_contact_name_a = None
    user_detail.emrg_contact_name_b = None
    user_detail.emrg_contact_mobile_a = None
    user_detail.emrg_contact_mobile_b = None
    user_detail.idcard_front_img = None
    user_detail.idcard_back_img = None
    user_detail.thirdparty_data = None
    user_detail.raise_comment = None
    user_detail.update_count = None
    user_detail.name_mirror = None
    user_detail.raise_amount_sign = None
    convert.add_one(user_detail)

    # 模拟event_id
    now = time.time()
    _event_id = str(company_id) + "_" + str(channel_id) + "_" + str(int(now * 1000))
    print("register_insert _event_id", _event_id)

    # 模拟token 取手机号的md5加密截取部分
    _token = user_password
    print("register_insert _event_id", _token)

    return dict(mobile=user_mobile, event_id=_event_id, token=_token)
