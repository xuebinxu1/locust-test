#!/user/bin/python3
# @Author:  LSY
# @Date:    2019/4/22
import pandas as pd
import os
from utils import bid_apply_time
import datetime
from random import choice
from config import data_fraud


def initial_all_user(is_read_file=False):
    """
    初始化操作,首先判断文件是否存在，如果存在则读取文件。否则进行初始化操作
    :param is_read_file: 初始化是否读取文件
    :return:
    """
    if is_read_file:
        file_path = './data.csv'
        data_exists = os.path.exists(file_path)
        if data_exists:
            user_df = pd.read_csv(file_path)
            return user_df
    else:
        total_user = data_fraud.TOTAL_REGISTERED_USER
        registered_users = [1 for _ in range(total_user)]
        registered_times = bid_apply_time.get_registered_time(total_user)
        user_df = pd.DataFrame(registered_users, columns=['registered'])
        user_df['registered_times'] = registered_times
        user_df['user_index'] = [i for i in range(total_user)]
        user_df['company_id'] = 110
        # initial channel id
        user_df = initial_user_channel(user_df)
        user_df['verified'] = initial_verified_users(total_user, data_fraud.USER_VERIFIED_RATE)
        user_df['carrier'] = initial_carrier_users(total_user, data_fraud.USER_CARRIER_RATE)
        user_df['bank_card'] = initial_bank_card_users(total_user, data_fraud.USER_BANK_CARD_RATE)
        user_df = initial_user_certification(user_df)
        user_df = bid_apply_time.get_bid_apply_time(user_df)
        user_df = initial_bid_apply_users(user_df, bid_apply_rate=data_fraud.USER_BID_APPLY_RATE)
        user_df = initial_loan_users(user_df, data_fraud.LOAN_RATE)
        user_df = initial_reject_users(user_df, reject_rate=data_fraud.REJECT_RATE)
        user_df = initial_repayment_users(user_df, repayment_rate=data_fraud.USER_REPAYMENT_RATE)
        user_df = initial_overdue_users(user_df)
        user_df = initial_overdue_repayment(user_df, overdue_repayment_rate=data_fraud.USER_OVERDUE_REPAYMENT_RATE)
        user_df = initial_overdue_within_3_days_repayment(user_df, data_fraud.USER_OVERDUE_WITHIN_3_DAYS_REPAYMENT_RATE)
        user_df = initial_overdue_4_to_7_days_repayment(user_df, data_fraud.USER_OVERDUE_4_TO_7_DAYS_REPAYMENT_RATE)
        user_df = initial_overdue_8_to_30_days_repayment(user_df, data_fraud.USER_OVERDUE_8_TO_30_DAYS_REPAYMENT_RATE)
        # 导出csv
        user_df.to_csv('./data.csv', index=False)
        return user_df


def initial_user_channel(df):
    """

    :param df: dataframe of all users
    :return:
    """
    total_users = df.shape[0]
    default_channel_user_count = round(total_users * data_fraud.DEFAULT_CHANNEL_RATE)
    zy8_channel_user_count = round(total_users * data_fraud.ZY8_CHANNEL_RATE)
    zy2_channel_user_count = round(total_users * data_fraud.ZY2_CHANNEL_RATE)
    zy7_channel_user_count = round(total_users * data_fraud.ZY7_CHANNEL_RATE)
    xp1_channel_user_count = round(total_users * data_fraud.XP1_CHANNEL_RATE)
    ay1_channel_user_count = round(total_users * data_fraud.AY1_CHANNEL_RATE)
    xl1_channel_user_count = total_users - default_channel_user_count - zy8_channel_user_count - zy2_channel_user_count - zy7_channel_user_count - xp1_channel_user_count - ay1_channel_user_count
    default_channel_id_list = [data_fraud.DEFAULT_CHANNEL_ID for _ in range(default_channel_user_count)]
    zy8_channel_id_list = [data_fraud.ZY8_CHANNEL_ID for _ in range(zy8_channel_user_count)]
    zy2_channel_id_list = [data_fraud.ZY2_CHANNEL_ID for _ in range(zy2_channel_user_count)]
    zy7_channel_id_list = [data_fraud.ZY7_CHANNEL_ID for _ in range(zy7_channel_user_count)]
    xp1_channel_id_list = [data_fraud.XP1_CHANNEL_ID for _ in range(xp1_channel_user_count)]
    ay1_channel_id_list = [data_fraud.AY1_CHANNEL_ID for _ in range(ay1_channel_user_count)]
    xl1_channel_id_list = [data_fraud.XL1_CHANNEL_ID for _ in range(xl1_channel_user_count)]
    df['channel_id'] = default_channel_id_list + zy8_channel_id_list + zy2_channel_id_list + zy7_channel_id_list + xp1_channel_id_list + ay1_channel_id_list + xl1_channel_id_list
    return df


def initial_verified_users(total_user, verified_rate):
    """
    初始化实名认证用户
    :param total_user: 所有用户
    :param verified_rate: 实名认证比率
    :return:
    """
    verified_users = round(total_user * verified_rate)
    un_verified_users = total_user - verified_users
    verified_users_list = [1 for _ in range(verified_users)]
    un_verified_users_list = [0 for _ in range(un_verified_users)]
    return verified_users_list + un_verified_users_list


def initial_carrier_users(total_user, carrier_rate):
    """
    初始化运营商认证用户
    :param total_user: 所有用户
    :param carrier_rate: 运营商认证比率
    :return:
    """
    carrier_users = round(total_user * carrier_rate)
    un_carrier_users = total_user - carrier_users
    carrier_users_list = [1 for _ in range(carrier_users)]
    un_carrier_users_list = [0 for _ in range(un_carrier_users)]
    return carrier_users_list + un_carrier_users_list


def initial_bank_card_users(total_user, bank_card_rate):
    """
    初始化银行卡认证用户
    :param total_user: 所有用户
    :param bank_card_rate: 银行卡认证比率
    :return:
    """
    bank_card_users = round(total_user * bank_card_rate)
    un_bank_card_users = total_user - bank_card_users
    bank_card_users_list = [1 for _ in range(bank_card_users)]
    un_bank_card_users_list = [0 for _ in range(un_bank_card_users)]
    return bank_card_users_list + un_bank_card_users_list


def initial_user_certification(df):
    """
    生成用户的认证项列表，方便插入认证项数据
    :param df: dataframe of all users
    :return:
    """
    certifications_df = df[['verified', 'carrier', 'bank_card']]
    verified = certifications_df['verified'].apply(lambda r: ['0'] if r == 1 else [])
    carrier = certifications_df['carrier'].apply(lambda r: ['1'] if r == 1 else [])
    bank_card = certifications_df['bank_card'].apply(lambda r: ['3'] if r == 1 else [])
    df['certifications'] = verified + carrier + bank_card
    return df


def initial_bid_apply_users(df, bid_apply_rate, verified='verified', carrier='carrier', bank_card='bank_card'):
    """
    初始化进件用户数量。 pre-condition: 实名认证、运营商认证、银行卡均通过
    :param df: dataframe of all users
    :param bid_apply_rate: 进件用户比率， 该比率 = 进件用户 / 总用户
    :param verified 实名认证
    :param carrier  运营商认证
    :param bank_card 银行卡认证
    :return:
    """
    # 满足进件的用户
    satisfy_bid_apply_users_df = df[(df[verified] == 1) & (df[carrier] == 1) & (df[bank_card] == 1)]
    actual_df = satisfy_bid_apply_users_df.sample(frac=bid_apply_rate)
    actual_df['bid_apply'] = 1
    df['bid_apply'] = actual_df['bid_apply']
    df = df.fillna(0)
    return df


def initial_loan_users(df, loan_rate, bid_apply_feature='bid_apply'):
    """
    初始化放款用户。pre-condition: 用户已经进行进件操作，且与放款操作是互斥的
    :param df: dataframe of all users
    :param bid_apply_feature: 进件
    :param loan_rate: 放款几率，该几率指的是进件单子中放款的用户几率
    :return:
    """
    # 筛选出已经进件的用户
    bid_apply_users_df = df[(df[bid_apply_feature] == 1)]
    bid_apply_users_count = bid_apply_users_df.shape[0]
    actual_loan_user = round(bid_apply_users_count * loan_rate)
    actual_loan_df = bid_apply_users_df.sample(frac=actual_loan_user/bid_apply_users_count)
    actual_loan_df['loan'] = 1
    df['loan'] = actual_loan_df['loan']
    df = df.fillna(0)
    loan_minutes = [i for i in range(60)]
    df['loan_times'] = df['bid_apply_times'].apply(
        lambda bid_apply_time: bid_apply_time + datetime.timedelta(minutes=choice(loan_minutes)))
    return df


def initial_reject_users(df, reject_rate, bid_apply_feature='bid_apply', loan_feature='loan'):
    """
    初始化拒件用户。 pre-condition: 用户已经进行进件操作，且与放款操作互斥
    :param df: dataframe of all users
    :param reject_rate: 进件用户比率
    :param bid_apply_feature: column name of bid apply
    :param loan_feature: column name of loan
    :return:
    """
    # 筛选出进件用户，然后过滤放款用户。
    bid_apply_user_df = df[df[bid_apply_feature] == 1]
    not_allow_loan_user_df = bid_apply_user_df[~(bid_apply_user_df[loan_feature] == 1)]
    # 在非放款用户下控制拒件的人数
    reject_user_df = not_allow_loan_user_df.sample(frac=reject_rate)
    reject_user_df['reject'] = 1
    df['reject'] = reject_user_df['reject']
    df = df.fillna(0)
    reject_seconds = [i for i in range(120)]
    df['reject_times'] = df['bid_apply_times'].apply(
        lambda bid_apply_time: bid_apply_time + datetime.timedelta(seconds=choice(reject_seconds)))
    return df


def initial_repayment_users(df, repayment_rate, loan_feature='loan'):
    """
    初始化还款用户。 pre-condition：用户已经进行放款操作
    :param df:  dataframe of all users
    :param loan_feature: column name of loan
    :param repayment_rate:还款几率，该几率是在放款单子的基础上的
    :return:
    """
    # 筛选出放款的单子
    loan_user_df = df[df[loan_feature] == 1]
    loan_user_count = loan_user_df.shape[0]
    repayment_user_count = round(loan_user_count * repayment_rate)
    repayment_user_df = loan_user_df.sample(frac=repayment_user_count/loan_user_count)
    repayment_user_df['repayment'] = 1
    df['repayment'] = repayment_user_df['repayment']
    df = df.fillna(0)
    # 随机产生用户还款日期列表
    repayment_days = [i for i in range(data_fraud.PRODUCT_PERIOD)]
    repayment_hours = [i for i in range(5)]
    repayment_seconds = [i for i in range(30)]
    df['repayment_times'] = df['loan_times'].apply(
        lambda loan_time: loan_time + datetime.timedelta(days=choice(repayment_days)) + datetime.timedelta(
            hours=choice(repayment_hours)) + datetime.timedelta(seconds=choice(repayment_seconds)))
    return df


def initial_overdue_users(df, loan_feature='loan', repayment_feature='repayment'):
    """
    初始化逾期用户。pre-condition：用户已经进行放款操作
    :param df: dataframe of all users
    :param loan_feature: column name of loan
    :param repayment_feature: column name of repayment
    :return:
    """
    # 筛选出放款的单子
    loan_user_df = df[df[loan_feature] == 1]
    # 筛选出未还款的单子
    overdue_user_df = loan_user_df[~(loan_user_df[repayment_feature] == 1)]
    overdue_user_df['overdue'] = 1
    df['overdue'] = overdue_user_df['overdue']
    df['overdue_times'] = df['loan_times'].apply(lambda time: time + datetime.timedelta(days=data_fraud.PRODUCT_PERIOD))
    df = df.fillna(0)
    return df


def initial_overdue_repayment(df, overdue_repayment_rate, overdue_feature='overdue'):
    """
    初始化逾期全额还款用户。逾期全额还款=逾期1-3天全额还款+逾期4-7天全额还款+逾期8-30天全额还款
    :param df: dataframe of all users
    :param overdue_repayment_rate: 逾期全额还款比率，该几率发生实在逾期单子的基础上的
    :param overdue_feature: column name of overdue
    :return:
    """
    # 筛选出逾期的单子
    overdue_users_df = df[df[overdue_feature] == 1]
    overdue_users_count = overdue_users_df.shape[0]
    overdue_repayment_user_count = round(overdue_users_count * overdue_repayment_rate)
    overdue_repayment_user_df = overdue_users_df.sample(frac=overdue_repayment_user_count/overdue_users_count)
    overdue_repayment_user_df['overdue_repayment'] = 1
    df['overdue_repayment'] = overdue_repayment_user_df['overdue_repayment']
    df = df.fillna(0)
    return df


def initial_overdue_within_3_days_repayment(df, overdue_within_3_days_repayment_rate, overdue_repayment_feature='overdue_repayment'):
    """
    初始化逾期1-3天全额还款的用户
    :param df: df of all users
    :param overdue_within_3_days_repayment_rate: 逾期1-3天全额还款比率，该几率发生是在逾期单子的基础上
    :param overdue_repayment_feature: column name of overdue
    :return:
    """
    # 筛选出逾期全额还款的所有单子
    overdue_repayment_users_df = df[df[overdue_repayment_feature] == 1]
    overdue_repayment_users_count = overdue_repayment_users_df.shape[0]
    overdue_within_3_days_repayment_user_count = round(
        overdue_repayment_users_count * overdue_within_3_days_repayment_rate)
    overdue_within_3_days_repayment_user_df = overdue_repayment_users_df.sample(
        frac=overdue_within_3_days_repayment_user_count / overdue_repayment_users_count)
    overdue_within_3_days_repayment_user_df['within_3_days_repayment'] = 1
    df['overdue_within_3_days_repayment'] = overdue_within_3_days_repayment_user_df['within_3_days_repayment']
    within_3_days_repayment_days = [i for i in range(3)]
    df['overdue_within_3_days_repayment_times'] = df['overdue_times'].apply(
        lambda time: time + datetime.timedelta(days=choice(within_3_days_repayment_days)))
    df = df.fillna(0)
    return df


def initial_overdue_4_to_7_days_repayment(df, overdue_4_to_7_days_repayment_rate, overdue_repayment_feature='overdue_repayment'):
    """
    初始化逾期4-7天全额还款的用户
    :param df: dataframe of all users
    :param overdue_4_to_7_days_repayment_rate: 逾期4-7天全额还款比率，该几率发生是在逾期单子的基础上
    :param overdue_repayment_feature: column name of overdue
    :return:
    """
    # 筛选出逾期全额还款的所有单子
    overdue_repayment_users_df = df[df[overdue_repayment_feature] == 1]
    overdue_repayment_users_count = overdue_repayment_users_df.shape[0]
    overdue_4_to_7_days_repayment_user_count = round(overdue_repayment_users_count * overdue_4_to_7_days_repayment_rate)
    overdue_4_to_7_days_repayment_user_df = overdue_repayment_users_df.sample(
        frac=overdue_4_to_7_days_repayment_user_count / overdue_repayment_users_count)
    overdue_4_to_7_days_repayment_user_df['4_to_7_days_repayment'] = 1
    df['overdue_4_to_7_days_repayment'] = overdue_4_to_7_days_repayment_user_df['4_to_7_days_repayment']
    overdue_4_to_7_days_repayment_days = [i for i in range(4, 8)]
    df['overdue_4_to_7_days_repayment_times'] = df['overdue_times'].apply(
        lambda time: time + datetime.timedelta(days=choice(overdue_4_to_7_days_repayment_days)))
    df = df.fillna(0)
    return df


def initial_overdue_8_to_30_days_repayment(df, overdue_8_to_30_days_repayment_rate, overdue_repayment_feature='overdue_repayment'):
    """
    初始化逾期8-30天全额还款的用户
    :param df: dataframe of all users
    :param overdue_8_to_30_days_repayment_rate: 逾期8-30 天全额还款比率，该几率发生是在逾期单子的基础上
    :param overdue_repayment_feature: column name of overdue
    :return:
    """
    # 筛选出逾期全额还款的所有单子
    overdue_repayment_users_df = df[df[overdue_repayment_feature] == 1]
    overdue_repayment_users_count = overdue_repayment_users_df.shape[0]
    overdue_8_to_30_days_repayment_user_count = round(overdue_repayment_users_count * overdue_8_to_30_days_repayment_rate)
    overdue_8_to_30_days_repayment_user_df = overdue_repayment_users_df.sample(
        frac=overdue_8_to_30_days_repayment_user_count / overdue_repayment_users_count)
    overdue_8_to_30_days_repayment_user_df['8_to_30_days_repayment'] = 1
    df['overdue_8_to_30_days_repayment'] = overdue_8_to_30_days_repayment_user_df['8_to_30_days_repayment']
    overdue_8_to_30_days_repayment_days = [i for i in range(8, 31)]
    df['overdue_8_to_30_days_repayment_times'] = df['overdue_times'].apply(
        lambda time: time + datetime.timedelta(days=choice(overdue_8_to_30_days_repayment_days)))
    df = df.fillna(0)
    return df


if __name__ == '__main__':
    import time
    begin = time.time()
    user_df = initial_all_user()
    print("total: %s" % str(time.time() - begin))