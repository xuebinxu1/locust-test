#!/user/bin/python3
# @Author:  LSY
# @Date:    2019/4/22
import pandas as pd
from datetime import datetime as dt
import datetime
from random import choice
import logging


time_normal_format = "%Y-%m-%d %H:%M:%S"
registered_normal_start_time = '09:00:00'
registered_normal_end_time = '15:00:00'


def get_registered_time(total, normal_rate=0.8):
    """
    生成注册时间
    :param total: 总人数
    :param normal_rate:正常时间段比率， 默认0.8
    :return:
    """
    normal_registered_datetime_list = get_normal_time(total_person=total, rate=normal_rate)
    normal_person = round(total * normal_rate)
    other_period_datetime_registered_list = get_other_period_time(total, normal_person)
    normal_registered_datetime_list.extend(other_period_datetime_registered_list)
    return normal_registered_datetime_list


def get_bid_apply_time(df):
    """
    获取进件时间
    :param df: dataframe of all users
    :return:
    """
    random_minutes = [i for i in range(10)]
    random_seconds = [i for i in range(30)]
    df['bid_apply_times'] = df['registered_times'].apply(
        lambda x: x + datetime.timedelta(minutes=choice(random_minutes)) + datetime.timedelta(
            seconds=choice(random_seconds)))
    return df


def get_normal_time(total_person, rate=0.8):
    """
    随机获取正常时间段的操作时间列表
    :param total_person: 所有用户
    :param rate: 正常时间段操作的人数比率
    :return: 时间列表
    """
    total_normal_person = round(total_person * rate)
    normal_list = pd.date_range(registered_normal_start_time, registered_normal_end_time, freq='S').tolist()
    normal_time_df = pd.DataFrame(normal_list, columns=['normal_time'])
    # 无放回抽样
    normal_time_list = normal_time_df['normal_time'].sample(total_normal_person, replace=False).tolist()
    normal_list = None
    normal_time_df = None
    return normal_time_list


def get_other_period_time(total_person, normal_period_person, splite_rate=0.8):
    """
    随机获取非正常时间段的操作时间列表
    :param total_person: 所有用户
    :param normal_period_person: 正常时间段操作的人数
    :param splite_rate: 非正常时间段有2个区间，一个是小于registered_normal_start_time, 一个是大于registered_normal_end_time
                该参数rate就是用来控制2个区间的人数的
    :return:时间列表
    """
    other_period_person_count = total_person - normal_period_person
    date_list = pd.date_range('01:00:00', registered_normal_start_time, freq='S').tolist()
    date_list1 = pd.date_range(registered_normal_end_time, '23:00:00', freq='S').tolist()
    early_operate_person_count = round(other_period_person_count * (1-splite_rate))
    late_operate_person_count = other_period_person_count - early_operate_person_count
    logging.info("get not normal time. total unnormal person: %s\tearly period person: %s\tlate period person: %s" % (total_person, early_operate_person_count, late_operate_person_count))
    other_period_time_df = pd.DataFrame(date_list, columns=['date_list'])
    other_period_time_df['date_list1'] = date_list1
    # 无放回抽样
    early_date_list = other_period_time_df['date_list'].sample(early_operate_person_count, replace=False).tolist()
    late_date_list = other_period_time_df['date_list1'].sample(late_operate_person_count, replace=False).tolist()
    early_date_list.extend(late_date_list)
    date_list = None
    date_list1 = None
    other_period_time_df = None
    return early_date_list


def trans_str_2_datetime(time, date_format=None):
    """
    str to datetime
    :param time: str of date
    :param date_format: date format
    :return:
    """
    if isinstance(time, str):
        if date_format is not None:
            time = dt.strptime(time, date_format)
        else:
            time = dt.strptime(time, time_normal_format)
    return time


def check_is_normal_time(time, normal_start_time, normal_end_time):
    """
    检查是否正常时间段
    :param time: 时间
    :return: true or false
    """
    if not isinstance(normal_end_time, dt):
        normal_start_time = dt.strptime(normal_start_time, time_normal_format)
        normal_end_time = dt.strptime(normal_end_time, time_normal_format)
    return normal_start_time <= time <= normal_end_time


def get_early_morning_time():
    """
    获取当天凌晨时间
    :return:
    """
    date = datetime.datetime.now()
    return datetime.datetime.now().replace(year=date.year, month=date.month, day=date.day, hour=0, minute=0, second=0)


if __name__ == "__main__":
    print(get_other_period_time(500, 0.2, 0.8))
    pass
    # today = datetime.datetime.today().strftime("%m/%d/%Y")
    # df = pd.date_range(today, periods=24, freq='H')
    # rand = np.random.rand(24)
    #
    # pass