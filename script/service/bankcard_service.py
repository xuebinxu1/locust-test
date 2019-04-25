from utils.my_snowflake import my_snow
from utils import convert, models
import requests

import random

# 中国邮政储蓄银行  中国工商银行 中国农业银行 中国银行 中国建设银行 中国交通银行
bankcard_prefix_list = ['621096', '620200', '622841', '621660', '621284', '622261']


def generate():
    bankcard_prefix = bankcard_prefix_list[random.randint(0, len(bankcard_prefix_list)) - 1]
    bankcard_last_six_digit = random.randint(0, 9999999999999)
    return bankcard_prefix + str(bankcard_last_six_digit).zfill(13)


# print(generate())

bank_list = {
    "CCB": "中国建设银行",
    "ABC": "中国农业银行",
    "ICBC": "中国工商银行",
    "BOC": "中国银行",
    "CMBC": "中国民生银行",
    "CMB": "招商银行",
    "CIB": "兴业银行",
    "BCM": "交通银行",
    "CITICIB": "中信银行",
    "PSBC": "中国邮政银行",
    "COMM": "中国交通银行",
}


def get_bank(cardNo):
    url = "https://ccdcapi.alipay.com/validateAndCacheCardInfo.json"
    params = {
        "_input_charset": "utf-8",
        "cardNo": cardNo,
        "cardBinCheck": "true",
    }
    try:
        bank_code = requests.get(url=url, params=params).json()["bank"]
    except:
        print('银行卡号输入有误！')
        return None
    dict_bank_info = dict()
    dict_bank_info['bank_name'] = bank_list[bank_code]
    dict_bank_info['bank_code'] = bank_code
    return dict_bank_info


def insert(mobile, company_id):
    """
    插入银行卡数据
    bankcard表造数据
    :return:
    """
    user = convert.query(models.User, mobile=mobile, company_id=company_id).first()
    # 一定要保证user表有数据
    if user is None:
        return
    print(user)
    user_detail = convert.query(models.UserDetail, mobile=mobile, company_id=company_id).first()
    bankcard_data = convert.query(models.Bankcard, mobile=mobile, company_id=company_id, is_default=1).first()
    payment_channel = convert.query(models.PaymentChannel, company_id=company_id, is_default=1).first()
    card_no = generate()
    dict_bank_info = get_bank(card_no)
    while dict_bank_info is None:
        card_no = generate()
        dict_bank_info = get_bank(card_no)
    bankcard = models.Bankcard()
    # 检查是否有默认卡
    if bankcard_data is None:
        bankcard.id = my_snow().get_next_id()
        bankcard.user_id = user.id
        bankcard.company_id = company_id
        bankcard.bank_code = dict_bank_info['bank_code']
        bankcard.bank_account_number = card_no
        bankcard.bank_account_name = user.name
        bankcard.bank_name = dict_bank_info['bank_name']
        bankcard.mobile = mobile
        bankcard.is_default = 1
        bankcard.payment_channel = payment_channel.payment_channel_name if payment_channel is not None else "富有"  # '支付渠道 富有, 易宝'
        bankcard.is_binding = 1  # '1 已绑定  0 已经解绑',
        bankcard.mchntcd = payment_channel.mchntcd
    else:
        bankcard.id = my_snow().get_next_id()
        bankcard.user_id = user.id
        bankcard.company_id = company_id
        bankcard.bank_code = dict_bank_info['bank_code']
        bankcard.bank_account_number = card_no
        bankcard.bank_account_name = user.name
        bankcard.bank_name = dict_bank_info['bank_name']
        bankcard.mobile = mobile
        bankcard.is_default = 0
        bankcard.payment_channel = payment_channel.payment_channel_name if payment_channel is not None else "富有"  # '支付渠道 富有, 易宝'
        bankcard.is_binding = 1  # '1 已绑定  0 已经解绑',
        bankcard.mchntcd = payment_channel.mchntcd
    if user_detail.bank_account_id is None:
        update = {'bank_account_id': card_no}
        convert.update_table(models.UserDetail, update, mobile=mobile, company_id=company_id)
    return convert.add_one(bankcard)

# insert(15180279540, 1)
