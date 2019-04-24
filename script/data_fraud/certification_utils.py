#!/user/bin/python3
# @Author:  LSY
# @Date:    2019/4/22

verified_type = 0
carrier_type = 1
bank_card_type = 2


def generate_certification(total_users, verified_rate, carrier_rate, bank_card_rate):
    """
    生成每个用户的认证项列表
    :param total_users: 所有用户
    :param verified_rate: 只进行到实名认证几率
    :param carrier_rate: 进行到运营商认证几率
    :param bank_card_rate: 进行到银行卡认证的几率
    :return:
    """
    user_certification_list = []
    verified_user_count = round(total_users * verified_rate)
    carrier_user_count = round(total_users * carrier_rate)
    bank_card_user_count = total_users - verified_user_count - carrier_user_count
    verified_user_list = [generate_user_certification_list(verified_type) for verified_user in range(verified_user_count)]
    carrier_user_list = [generate_user_certification_list(carrier_type) for carrier_user in range(carrier_user_count)]
    bank_card_user_list = [generate_user_certification_list(bank_card_type) for bank_card_user in bank_card_user_count]
    user_certification_list.extend(verified_user_list)
    user_certification_list.extend(carrier_user_list)
    user_certification_list.extend(bank_card_user_list)
    return user_certification_list


def certification(certification_list):
    """
    执行认证操作
    :param certification_list: 待认证的列表
    """
    for certification_type in certification_list:
        if certification_type == verified_type:
            pass
        elif certification_type == carrier_type:
            pass
        elif certification_type == bank_card_type:
            pass
    # 检查该用户的流程是否结束,如果结束：返回false。 否则，返回True，继续进件流程
    if check_is_end(certification_list):
        return True
    return False


def generate_user_certification_list(certification_list_type):
    """
    生成用户的认证列表
    :param certification_list_type 待认证列表的类型
    :return:
    """
    if certification_list_type == 0:
        return [0]
    elif certification_list_type == 1:
        return [0, 1]
    elif certification_list_type == 3:
        return [0, 1, 3]
    else:
        return []


def check_is_end(certification_type_list):
    """
    判断用户是否继续下一步流程。 验证类型小于2，说明该用户认证流程没走完
    :param certification_type_list: 验证类型列表
    :return:
    """
    if len(certification_type_list) < 2:
        return False
    return True
