#!/user/bin/python3
# @Author:  LSY
# @Date:    2019/4/24
from script.data_fraud.data_initial import initial_all_user
import datetime
from script.data_fraud.service import registered_and_bid_apply_service
from multiprocessing import Process, Manager
from utils import bid_apply_time
from script.data_fraud.service import autonym_service


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
        # loan_process = Process(target=loan, args=(user_df, 'loan', share_event_id_dict))
        # reject_process = Process(target=reject, args=(user_df, 'reject', share_event_id_dict))
        # repayment_process = Process(target=repayment, args=(user_df, 'repayment', share_event_id_dict))
        # overdue_and_repayment_process = Process(target=overdue_and_repayment, args=(user_df, share_event_id_dict))
        registered_process.start()
        # loan_process.start()
        # reject_process.start()
        # repayment_process.start()
        # overdue_and_repayment_process.start()
        p_list.append(registered_process)
        # p_list.append(loan_process)
        # p_list.append(reject_process)
        # p_list.append(repayment_process)
        # p_list.append(overdue_and_repayment_process)
        for res in p_list:
            res.join()
        print(share_event_id_dict)


def registered(df, registered, share_dict=None):
    """
    注册
    :param df: dataframe of all users
    :param registered: column name of registered
    :param share_dict: 用于进程间的共享数据 {user_index: event_id}
    :return:
    """
    if share_dict is None:
        share_dict = {}
    company_id_column = 'company_id'
    channel_id_column = 'channel_id'
    registered_times_column = 'registered_times'
    user_index_column = 'user_index'
    mobile_platform_column = 'mobile_platform'
    verified_column = 'verified'
    carrier_column = 'carrier'
    bank_card_column = 'bank_card'
    bid_apply_column = 'bid_apply'
    registered_df = df[[registered, registered_times_column, company_id_column, channel_id_column, user_index_column, mobile_platform_column, verified_column, carrier_column, bank_card_column, bid_apply_column]]
    registered_times = registered_df[registered_times_column].apply(lambda time: str(time)).tolist()
    user_index_list = registered_df[user_index_column].tolist()
    user_mapping_dict = dict(zip(registered_times, user_index_list))
    start = bid_apply_time.get_early_morning_time()
    total = 0
    is_end_list = registered_times[:]
    largest_time = get_largest_time(is_end_list)
    while True:
        start = start.strftime("%Y-%m-%d %H:%M:%S")
        if start in registered_times:
            user_index = user_mapping_dict[start]
            current_user = registered_df[registered_df[user_index_column] == user_index]
            mobile_platform = int(current_user[mobile_platform_column])
            is_verified = True if int(current_user[verified_column]) == 1 else False
            is_carrier = True if int(current_user[carrier_column]) == 1 else False
            is_bank_card = True if int(current_user[bank_card_column]) == 1 else False
            is_bid_apply = True if int(current_user[bid_apply_column]) == 1 else False
            company_id = int(registered_df[registered_df[user_index_column] == user_index][company_id_column])
            channel_id = int(registered_df[registered_df[user_index_column] == user_index][channel_id_column])
            # 注册
            mobile, token, event_id = registered_and_bid_apply_service.register_and_login(company_id, channel_id, mobile_platform)
            user_info = dict(event_id=event_id, token=token)
            share_dict[user_index] = user_info
            # 认证并进件
            certifications_and_bid_apply(event_id, company_id, channel_id, mobile, token, is_verified, is_carrier, is_bank_card, is_bid_apply)
            total += 1
        elif start > largest_time:
            break
        # time.sleep(1)
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=1)
    print(total)


def certifications_and_bid_apply(event_id, company_id, channel_id, mobile, token, is_verified=False, is_carrier=False, is_bank_card=False, is_bid_apply=False):
    try:
        # 有盾回调
        registered_and_bid_apply_service.youdun_recognize_callback(event_id)
        # sdk上传
        registered_and_bid_apply_service.sdk_callback(event_id)
        # 实名认证
        cid = None
        name = None
        if is_verified:
            cid, name = autonym_service.request_profile_validation(company_id, channel_id, event_id, mobile, token)
        # 运营商认证
        if is_carrier:
            registered_and_bid_apply_service.moxie_callback(event_id, mobile)
            registered_and_bid_apply_service.carrier(token, company_id, channel_id, mobile, event_id)
        # 银行卡认证
        if is_bank_card:
            registered_and_bid_apply_service.add_bankcard(event_id, company_id, channel_id, mobile, token, name, cid)
        # 进件
        if is_bid_apply:
            registered_and_bid_apply_service.choose_bankcard(event_id, company_id, channel_id, mobile, token)
            registered_and_bid_apply_service.bid_application(event_id, company_id, channel_id, mobile, token)
    except Exception as e:
        print("发生异常 event_id: %s   message: %s" % (event_id, e))
        pass


def loan(df, loan, share_dict=None):
    """
    用户放款操作，即审核通过
    :param loan: column name of loan
    :param share_dict: 进程间共享的数据 {user_index: event_id}
    :return:
    """
    if share_dict is None:
        share_dict = {}
    company_id_column = 'company_id'
    channel_id_column = 'channel_id'
    user_index_column = 'user_index'
    loan_times_column = 'loan_times'
    loan_df = df[df[loan] == 1][[loan, loan_times_column, company_id_column, channel_id_column, user_index_column]]
    loan_times_list = loan_df[loan_times_column].tolist()
    user_index_list = loan_df[user_index_column].tolist()
    user_mapping_dict = dict(zip(loan_times_list, user_index_list))
    start = bid_apply_time.get_early_morning_time()
    is_end_list = loan_times_list[:]
    largest_time = get_largest_time(is_end_list)
    while True:
        start = start.strftime("%Y-%m-%d %H:%M:%S")
        if start in loan_times_list:
            user_index = user_mapping_dict[start]
            event_id = share_dict[user_index]['event_id']
            pass
        elif start > largest_time:
            break
        # time.sleep(1)
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=1)


def reject(df, reject, share_dict=None):
    """
    用户拒件操作
    :param df: dataframe of all users
    :param reject: column name of reject
    :param share_dict: 进程间共享的数据 {user_index: event_id}
    :return:
    """
    if share_dict is None:
        share_dict = {}
    company_id_column = 'company_id'
    channel_id_column = 'channel_id'
    user_index_column = 'user_index'
    reject_times_column = 'reject_times'
    reject_df = df[df[reject] == 1][[reject, reject_times_column, company_id_column, channel_id_column, user_index_column]]
    reject_times_list = reject_df[reject_times_column].tolist()
    user_index_list = reject_df[user_index_column].tolist()
    user_mapping_dict = dict(zip(reject_times_list, user_index_list))
    start = bid_apply_time.get_early_morning_time()
    is_end_list = reject_times_list[:]
    largest_time = get_largest_time(is_end_list)
    while True:
        start = start.strftime("%Y-%m-%d %H:%M:%S")
        if start in reject_times_list:
            user_index = user_mapping_dict[start]
            event_id = share_dict[user_index]['event_id']
            pass
        elif start > largest_time:
            break
        # time.sleep(1)
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=1)


def repayment(df, repayment, share_dict=None):
    """
    正常还款操作
    :param df: dataframe of all users
    :param repayment: column name of repayment
    :param share_dict: 进程间共享的数据 {user_index: event_id}
    :return:
    """
    if share_dict is None:
        share_dict = {}
    company_id_column = 'company_id'
    channel_id_column = 'channel_id'
    user_index_column = 'user_index'
    repayment_times_column = 'repayment_times'
    repayment_df = df[df[repayment] == 1][
        [repayment, repayment_times_column, company_id_column, channel_id_column, user_index_column]]
    repayment_times_list = repayment_df[repayment_times_column].tolist()
    user_index_list = repayment_df[user_index_column].tolist()
    user_mapping_dict = dict(zip(repayment_times_list, user_index_list))
    start = bid_apply_time.get_early_morning_time()
    is_end_list = repayment_times_list[:]
    largest_time = get_largest_time(is_end_list)
    while True:
        start = start.strftime("%Y-%m-%d %H:%M:%S")
        if start in repayment_times_list:
            user_index = user_mapping_dict[start]
            event_id = share_dict[user_index]['event_id']
            token = share_dict[user_index]['token']
            # 还款
            pass
        elif start > largest_time:
            break
        # time.sleep(1)
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=1)


def overdue_and_repayment(df, share_dict=None):
    """
    逾期还款操作(全部还款)
    :param df: dataframe of all users
    :param share_dict: 进程间共享的数据 {user_index: event_id}
    :return: 
    """
    if share_dict is None:
        share_dict = {}
    company_id_column = 'company_id'
    channel_id_column = 'channel_id'
    user_index_column = 'user_index'
    overdue_within_3_days_repayment_column = 'overdue_within_3_days_repayment'
    overdue_within_3_days_repayment_times_column = 'overdue_within_3_days_repayment_times'
    overdue_4_to_7_days_repayment_column = 'overdue_4_to_7_days_repayment'
    overdue_4_to_7_days_repayment_times_column = 'overdue_4_to_7_days_repayment_times'
    overdue_8_to_30_days_repayment_column = 'overdue_8_to_30_days_repayment'
    overdue_8_to_30_days_repayment_times_column = 'overdue_8_to_30_days_repayment_times'
    overdue_within_3_days_repayment_df = df[df[overdue_within_3_days_repayment_column] == 1][[overdue_within_3_days_repayment_column, overdue_within_3_days_repayment_times_column, company_id_column, channel_id_column, user_index_column]]
    overdue_4_to_7_days_repayment_df = df[df[overdue_4_to_7_days_repayment_column] == 1][[overdue_4_to_7_days_repayment_column, overdue_4_to_7_days_repayment_times_column, company_id_column, channel_id_column, user_index_column]]
    overdue_8_to_30_days_repayment_df = df[df[overdue_8_to_30_days_repayment_column] == 1][[overdue_8_to_30_days_repayment_column, overdue_8_to_30_days_repayment_times_column, company_id_column, channel_id_column, user_index_column]]
    overdue_within_3_days_repayment_user_index_list = overdue_within_3_days_repayment_df[user_index_column].tolist()
    overdue_within_3_days_repayment_times_list = overdue_within_3_days_repayment_df[overdue_within_3_days_repayment_times_column].tolist()
    overdue_4_to_7_days_repayment_user_index_list = overdue_4_to_7_days_repayment_df[user_index_column].tolist()
    overdue_4_to_7_days_repayment_times_list = overdue_4_to_7_days_repayment_df[overdue_4_to_7_days_repayment_times_column].tolist()
    overdue_8_to_30_days_repayment_user_index_list = overdue_8_to_30_days_repayment_df[user_index_column].tolist()
    overdue_8_to_30_days_repayment_times_list = overdue_8_to_30_days_repayment_df[overdue_8_to_30_days_repayment_times_column].tolist()
    user_index_list = overdue_within_3_days_repayment_user_index_list + overdue_4_to_7_days_repayment_user_index_list + overdue_8_to_30_days_repayment_user_index_list
    times_list = overdue_within_3_days_repayment_times_list + overdue_4_to_7_days_repayment_times_list + overdue_8_to_30_days_repayment_times_list
    user_mapping_dict = dict(zip(times_list, user_index_list))
    start = bid_apply_time.get_early_morning_time()
    is_end_list = times_list[:]
    largest_time = get_largest_time(is_end_list)
    while True:
        start = start.strftime("%Y-%m-%d %H:%M:%S")
        if start in times_list:
            user_index = user_mapping_dict[start]
            event_id = share_dict[user_index]['event_id']
            token = share_dict[user_index]['token']
            # 还款
        elif start > largest_time:
            break
        # time.sleep(1)
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=1)


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


def get_largest_time(times_list):
    """
    获取列表中最大的时间日期
    :param times_list:
    :return:
    """
    if times_list is None:
        return None
    times_list.sort(reverse=True)
    return times_list[0]


if __name__ == '__main__':
    launch()
