from utils.my_snowflake import my_snow
from utils import convert, models


def select():
    """
    测试类
    :return:
    """
    dict_params = dict()
    dict_params['mobile'] = 18857119819
    dict_params['company_id'] = 1
    record_list = convert.query(models.UserCertification, mobile=18857119819).all()
    print(len(record_list))
    print(record_list[0].status)


# select()

def insert_autonym(mobile, company_id):
    """
    0实名认证
    user_certification表造数据
    :return:
    """
    user = convert.query(models.User, mobile=mobile, company_id=company_id).first()
    print(user)
    user_certification = models.UserCertification()
    user_certification.id = my_snow().get_next_id()
    user_certification.channel_id = user.register_channel_id
    user_certification.status = 1  # 成功
    user_certification.succeed_flag = 1  # 成功
    user_certification.type = 0  # 0:实名认证，1运营商认证，3银行卡认
    user_certification.expiration_period = 7  # 7实名认证，30运营商认证，-1银行卡认
    user_certification.mobile = mobile
    user_certification.company_id = company_id

    return convert.add_one(user_certification)


# insert_autonym(15180279540, 1)


def insert_operator(mobile, company_id):
    """
    1运营商认证
    user_certification表造数据
    :return:
    """
    user = convert.query(models.User, mobile=mobile, company_id=company_id).first()
    user_certification = models.UserCertification()
    user_certification.id = my_snow().get_next_id()
    user_certification.channel_id = user.register_channel_id
    user_certification.status = 1  # 成功
    user_certification.succeed_flag = 1  # 成功
    user_certification.type = 1  # 0:实名认证，1运营商认证，3银行卡认
    user_certification.expiration_period = 30  # 7实名认证，30运营商认证，-1银行卡认
    user_certification.mobile = mobile
    user_certification.company_id = company_id
    return convert.add_one(user_certification)


# insert_operator(15180279540, 1)


def insert_bankcard(mobile, company_id):
    """
    3银行卡认证
    user_certification表造数据
    :return:
    """
    user = convert.query(models.User, mobile=mobile, company_id=company_id).first()
    user_certification = models.UserCertification()
    user_certification.id = my_snow().get_next_id()
    user_certification.channel_id = user.register_channel_id
    user_certification.status = 1  # 成功
    user_certification.succeed_flag = 1  # 成功
    user_certification.type = 3  # 0:实名认证，1运营商认证，3银行卡认
    user_certification.expiration_period = -1  # 7实名认证，30运营商认证，-1银行卡认
    user_certification.mobile = mobile
    user_certification.company_id = company_id
    return convert.add_one(user_certification)


# insert_bankcard(15180279540, 1)


def update_cert_item(mobile, company_id, cert_item_list):
    """
    更新user_detail的认证项
    user_detail表造数据
    :return:
    """
    update = {'cert_item': ",".join(cert_item_list)}

    return convert.update_table(models.UserDetail, update, mobile=mobile, company_id=company_id)


# update_cert_item(15180279540, 1, ['0', '1'])


def update_cert_item_of_user_apply_info(mobile, company_id, cert_item_list):
    """
    更新user_apply_info的认证项
    user_apply_info表造数据
    :return:
    """
    update = {'cert_item': ",".join(cert_item_list)}

    return convert.update_table(models.UserApplyInfo, update, mobile=mobile, company_id=company_id)

# update_cert_item_of_user_apply_info(15180279540, 1, ['0', '1', '3'])
