#!/user/bin/python3
# @Author:  LSY
# @Date:    2019/4/24
from utils.bid_apply_utils import initial_all_user


def launch():
    """
    启动脚本。
    """
    # 初始化用户数据
    initial_all_user()


def registered(df, registered, registered_times):
    """
    注册
    :param df: dataframe of all users
    :param registered: column name of registered
    :param registered_times:  column name of registered time
    :return:
    """
    registered_df = df[[registered, registered_times]]
    df['event_id'] = registered_df.apply(lambda user: print(user[registered_times]), axis=1)
    return df


def verified(df, event_id, verified):
    """
    用户实名认证
    :param df: dataframe of all users
    :param event_id: user event_id
    :param verified: column name of verified
    :return:
    """
    verified_df = df[df[verified] == 1]
    verified_df.apply(lambda user: print(user[event_id]), axis=1)


def carrier(df, event_id, carrier):
    """
    用户运营商认证
    :param df: dataframe of all users
    :param event_id: column name of event_id
    :param carrier: column name of carrier
    :return:
    """
    carrier_df = df[df[carrier] == 1]
    carrier_df.apply(lambda user: print(user[event_id]), axis=1)


def bank_card(df, event_id, bank_card):
    """
    银行卡认证
    :param df: dataframe of all users
    :param event_id: column name of event_id
    :param bank_card: column name of bank_card
    :return:
    """
    bank_card_df = df[df[bank_card] == 1]
    bank_card_df.apply(lambda user: print(user[event_id]))


def bid_apply(df, event_id, bid_apply):
    """
    用户进件
    :param df: dataframe of all users
    :param event_id:  column name of event_id
    :param bid_apply:  column name of bank_card
    :return: 
    """
    bid_apply_df = df[df[bid_apply] == 1]
    df['bid_id'] = bid_apply_df.apply(lambda user: print(user[event_id], user['bid_apply_times']), axis=1)
    return df


def loan(df, event_id, bid_id, loan):
    """
    给用户放款
    :param df: dataframe of all users
    :param event_id: column name of event_id
    :param bid_id: column name of bid_id
    :param loan: column name of loan operate
    :return:
    """
    loan_df = df[df[loan] == 1]
    loan_df.apply(lambda user: print(user[event_id], user[bid_id], user['loan_times']), axis=1)


def reject(df, event_id, bid_id, reject):
    """
    拒件操作
    param df: dataframe of all users
    :param event_id: column name of event_id
    :param bid_id: column name of bid_id
    :param reject: column name of reject
    :return:
    """
    reject_df = df[df[reject] == 1]
    reject_df.apply(lambda user: print(user[event_id], user[bid_id], user['reject_times']), axis=1)


def repayment(df, event_id, bid_id, repayment):
    """
    正常还款操作
    :param df: dataframe of all users
    :param event_id: column name of event_id
    :param bid_id: column name of bid_id
    :param repayment: column name of repayment
    :return:
    """
    repayment_df = df[df[repayment] == 1]
    repayment_df.apply(lambda user: print(user[event_id], user[bid_id], user['repayment_times']), axis=1)


def overdue(df, event_id, bid_id, overdue):
    """
    逾期操作
    :param df: dataframe of all users
    :param event_id: column name of event_id
    :param bid_id: column name of bid_id
    :param overdue: column name of overdue
    :return:
    """
    overdue_df = df[df[overdue] == 1]
    overdue_df.apply(lambda user: print(user[event_id], user[bid_id], user['overdue_times']), axis=1)


def overdue_within_3_days_repayment(df, event_id, bid_id, overdue_within_3_days_repayment):
    """
    逾期3天内还款操作
    :param df: dataframe of all users
    :param event_id: column name of event_id
    :param bid_id: column name of bid_id
    :param overdue_within_3_days_repayment: column name of overdue_within_3_days_repayment
    :return: 
    """
    overdue_within_3_days_repayment_df = df[df[overdue_within_3_days_repayment] == 1]
    overdue_within_3_days_repayment_df.apply(
        lambda user: print(user[event_id], user[bid_id], user['overdue_within_3_days_repayment_times']), axis=1)


def overdue_4_to_7_days_repayment(df, event_id, bid_id, overdue_4_to_7_days_repayment):
    """
    逾期3天内还款操作
    :param df: dataframe of all users
    :param event_id: column name of event_id
    :param bid_id: column name of bid_id
    :param overdue_4_to_7_days_repayment: column name of overdue_4_to_7_days_repayment
    :return:
    """
    overdue_4_to_7_days_repayment_df = df[df[overdue_4_to_7_days_repayment] == 1]
    overdue_4_to_7_days_repayment_df.apply(
        lambda user: print(user[event_id], user[bid_id], user['overdue_4_to_7_days_repayment_times']), axis=1)


def overdue_8_to_30_days_repayment(df, event_id, bid_id, overdue_8_to_30_days_repayment):
    """
    逾期3天内还款操作
    :param df: dataframe of all users
    :param event_id: column name of event_id
    :param bid_id: column name of bid_id
    :param overdue_8_to_30_days_repayment: column name of overdue_8_to_30_days_repayment
    :return:
    """
    overdue_8_to_30_days_repayment_df = df[df[overdue_8_to_30_days_repayment] == 1]
    overdue_8_to_30_days_repayment_df.apply(
        lambda user: print(user[event_id], user[bid_id], user['within_3_days_repayment_times']), axis=1)
