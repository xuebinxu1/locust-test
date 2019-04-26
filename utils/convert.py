# coding=utf-8
from utils.models import DBSession
from datetime import datetime

session = DBSession()


def query(table, *criterion, **params):
    """
    查询单条或者多条数据
    :param table:  数据库表映射对象
    :param criterion:   查询条件
    :return:  查询得到的一条或者多条数据
    """
    if criterion is not None:
        if len(criterion) > 0 and criterion[0] is None:
            criterion = tuple()

    condition = list(map(lambda x: table.__dict__[x] == params[x], params))
    condition.extend(criterion)
    result = session.query(table).filter(*condition)
    session.close()
    return result


def add_one(model):
    """
    插入一条或者多条数据
    :param tables: 数据库表映射对象
    :return: 插入的一条或者多条数据的主键,以list形式返回
    """
    session.add(model)
    session.commit()
    session.flush()
    session.close()
    return model


def add_all(tables):
    """
    插入一条或者多条数据
    :param tables: 数据库表映射对象
    :return: 插入的一条或者多条数据的主键,以list形式返回
    """
    session.add_all(tables)
    session.commit()
    session.close()
    return tables


def update_table(table, update, **criterion):
    """
    更新指定的数据库表,可以更新一条或者多条数据
    取决于criterion能否帮助filter得到多条数据
    :param table:  数据库表隐射对象
    :param update: 要更新的字段
    :param criterion: 获取数据的条件
    :return: 更新的数据的条目数
    """
    update['gmt_modified'] = datetime.now()
    condition = list(map(lambda x: table.__dict__[x] == criterion[x], criterion))
    result = session.query(table).filter(*condition).update(update)
    session.commit()
    session.close()
    return result
