import random
import config.constant as constant
from script.credit.cid_generator import generate as cid_generate
import requests


def request_profile_validation(event_id, mobile, token):
    """
    实名认证
    :param event_id:
    :param mobile:
    :param token:
    :return:
    """
    company_id = "200"
    channel_id = "0"
    education_level = random.randint(0, 3)
    marital_status = random.randint(0, 4)
    income_level = random.randint(0, 6)
    front_img_url = constant.TEST_OSS_URL + '/' + (str(mobile) + 'front')
    back_img_url = constant.TEST_OSS_URL + '/' + (str(mobile) + 'back')
    living_test_result = random.choice([0, 1])
    emrg_contact_name_a = "某某A"
    emrg_contact_mobile_a = 13700000001
    emrg_contact_name_b = "某某B"
    emrg_contact_mobile_b = 13700000002
    province = random.choice(
        ['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北',
         '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '台湾', '香港', '澳门'])
    city = '市中心'
    address = '宇宙中心'
    name = "某某"
    headers = {"token": token}

    profile_req_body = dict(mobile=mobile, companyId=company_id, channelId=channel_id,
                            name=name, cid=cid_generate(), educationLevel=education_level,
                            maritalStatus=marital_status, incomeLevel=income_level, frontImage=front_img_url,
                            backImage=back_img_url, livingTestResult=living_test_result,
                            emrgContactNameA=emrg_contact_name_a, emrgContactMobileA=emrg_contact_mobile_a,
                            emrgContactNameB=emrg_contact_name_b, emrgContactMobileB=emrg_contact_mobile_b,
                            province=province, city=city, detailedAddress=address,
                            eventId=event_id)
    url = constant.ICEWINE_BASE_URL_200 + '/profile/upload'
    # files:接口中需要上传文件则需要用到该参数
    r = requests.post(url, data=profile_req_body, headers=headers)
    # print(r.text.encode('utf-8'))
    print(str(mobile) + "实名认证请求")
    dict_data = dict()
    dict_data['event_id'] = event_id
    dict_data['mobile'] = mobile
    dict_data['token'] = token
    return dict_data
