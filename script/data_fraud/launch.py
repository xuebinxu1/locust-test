#!/user/bin/python3
# @Author:  LSY
# @Date:    2019/4/24
from script.data_fraud.data_initial import initial_all_user
import schedule
import datetime
from script.demo.util import UserUtil
from multiprocessing import Process, Manager
from utils import bid_apply_time
import time


def launch():
    """
    启动脚本。
    """
    # 初始化用户数据
    user_df = initial_all_user()
    # 初始化Manager字典，用于进程间的数据共享
    with Manager() as manager:
        share_event_id_dict = manager.dict()
        p_list = []
        registered_process = Process(target=registered, args=(user_df, 'registered', share_event_id_dict))
        registered_process.start()
        p_list.append(registered_process)
        for res in p_list:
            res.join()
        print(share_event_id_dict)


def registered(df, registered, share_dict={}):
    """
    注册
    :param df: dataframe of all users
    :param registered: column name of registered
    :param share_dict: 用于进程间的共享数据
    :return:
    """
    company_id_column = 'company_id'
    channel_id_column = 'channel_id'
    registered_times_column = 'registered_times'
    user_index_column = 'user_index'
    registered_df = df[[registered, registered_times_column, company_id_column, channel_id_column, user_index_column]]
    registered_times = registered_df[registered_times_column].apply(lambda time: str(time)).tolist()
    user_index_list = registered_df[user_index_column].tolist()
    user_mapping_dict = dict(zip(registered_times, user_index_list))
    start = bid_apply_time.get_early_morning_time()
    total = 0
    while True:
        start = start.strftime("%Y-%m-%d %H:%M:%S")
        if start in registered_times:
            user_index = user_mapping_dict[start]
            company_id = int(registered_df[registered_df[user_index_column] == user_index][company_id_column])
            channel_id = int(registered_df[registered_df[user_index_column] == user_index][channel_id_column])
            # 注册
            mobile, event_id = UserUtil.register(company_id, channel_id)
            # 认证
            certifications(event_id)
            share_dict[user_index] = start
            print(start, user_index)
            total += 1
        elif datetime.datetime.now().hour == 23 and datetime.datetime.now().minute == 1:
            # 23点后退出
            break
        elif datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S").hour == 23:
            break
        time.sleep(1)
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=1)
    print(total)


def certifications(event_id):
    print(event_id)
    pass


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


def bid_apply(df, bid_apply, share_dict):
    """
    用户进件
    :param df: dataframe of all users
    :param bid_apply:  column name of bank_card
    :param share_dict: 进程间共享的数据
    :return: 
    """
    # 筛选出进件单子
    bid_apply_df = df[df[bid_apply] == 1]
    bid_apply_times_column = 'bid_apply_times'
    user_index_column = 'user_index'
    bid_apply_time_list = bid_apply_df[bid_apply_times_column].apply(lambda time: str(time)).tolist()
    user_index_list = bid_apply_df[user_index_column].tolist()
    user_mapping_dict = dict(zip(bid_apply_time_list, user_index_list))
    start = bid_apply_time.get_early_morning_time()
    while True:
        start = start.strftime("%Y-%m-%d %H:%M:%S")
        if start in bid_apply_time_list:
            user_index = user_mapping_dict[start]
            # 进件
            event_id = share_dict[user_index]
            
            share_dict[user_index] = start
            print(start, user_index)
        elif datetime.datetime.now().hour == 23 and datetime.datetime.now().minute == 1:
            # 23点后退出
            break
        elif datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S").hour == 23:
            break
        time.sleep(1)
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=1)
        pass
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


def change_date_to_time(date):
    """
    将日期转为日分秒形式。 '2019-04-25 00:00:00' -》'00:00:00'
    :param date: 日期
    :return:
    """
    try:
        time = str(date).split(' ')[1]
    except Exception:
        time = '09:00:00'
    return time


if __name__ == '__main__':
    launch()
