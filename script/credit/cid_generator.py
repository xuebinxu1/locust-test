import random
from datetime import timedelta, date
import datetime
import requests
import json

codelist = ['330225', '330202']


def generate():
    """
      随机生成身份证号，sex = 0表示女性，sex = 1表示男性
      """
    sex = random.randint(0, 1)
    # 随机生成一个区域码(6位数)
    id_number = codelist[random.randint(0, len(codelist)) - 1]  # 地区项
    # 限定出生日期范围(8位数)
    start, end = "1970-01-01", "2000-12-30"
    days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
    birth_days = datetime.datetime.strftime(
        datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days)), "%Y%m%d"
    )
    id_number += str(birth_days)
    # 顺序码(2位数)
    id_number += str(random.randint(10, 99))
    # 性别码(1位数)
    id_number += str(random.randrange(sex, 10, step=2))
    # 校验码(1位数)
    return id_number + str(get_check_digit(id_number))


def get_check_digit(id_number):
    """通过身份证号获取校验码"""
    check_sum = 0
    for i in range(0, 17):
        check_sum += ((1 << (17 - i)) % 11) * int(id_number[i])
    check_digit = (12 - (check_sum % 11)) % 11
    return check_digit if check_digit < 10 else 'X'


# print(generate())
# company_id = "1"
# channel_id = "0"
# header = {"token": "a4bee62dd4d5536a67bc07acd02dcb6448a8115909ae907d2411be6620d7fefa"}
# data = dict(companyId=company_id, channelId=channel_id, mobile='13700000809', eventId='1_0_13700000809_1550127129817')
# response_dict = json.loads(requests.get(url='http://localhost:6100/icewine/carrier/status', headers=header,
#                                         params=data).content)
# print(response_dict)
