from utils import convert, models
from datetime import datetime
from utils.my_snowflake import my_snow
import random


def get_contract_no():
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    num = random.randint(0, 999999999999999)
    return str(year) + str(month) + str(day) + str(num)


def get_transaction(contract_no, bid, event_id, status):
    transaction = models.Transaction()
    transaction.id = my_snow().get_next_id()
    transaction.company_id = bid.company_id
    transaction.contract_no = contract_no
    transaction.type = 2
    transaction.scene = 2
    transaction.status = status
    transaction.amount = bid.amount
    transaction.customer_name = datetime.now()
    transaction.mobile = bid.mobile
    transaction.bid_id = bid.id
    transaction.bid_contract_no = bid.contract_no
    transaction.payment_channel = "富友"
    transaction.payment_channel_id = 2
    transaction.event_id = event_id
    transaction.channel_id = bid.channel_id
    transaction.transaction_time = datetime.now()
    transaction.comment = None
    return transaction


def operate(event_id, bid_id):
    """
    正常还款 线上
    更新bid表、插入bid_workflow记录
    :return:
    """
    update = {'status': 7, 'repayment_time_type': 1, 'repayment_approach_type': 1, 'repayment_credit_type': 1}
    bid = convert.query(models.Bid, id=bid_id).first()
    contract_no = get_contract_no()
    # 插入bid_workflow记录
    bid_workflow = models.BidWorkflow()
    bid_workflow.id = my_snow().get_next_id()
    bid_workflow.company_id = bid.company_id
    bid_workflow.bid_id = bid.id
    bid_workflow.user_id = bid.user_id
    bid_workflow.last_status = 3
    bid_workflow.current_status = 7
    bid_workflow.operator_id = 0
    bid_workflow.operating_time = datetime.now()
    bid_workflow.action = "还款"
    bid_workflow.suggestion = None
    bid_workflow.channel_id = bid.channel_id
    # 插入current_transaction记录
    current_transaction = models.CurrentTransaction()
    current_transaction.id = my_snow().get_next_id()
    current_transaction.company_id = bid.company_id
    current_transaction.contract_no = contract_no
    current_transaction.type = 2
    current_transaction.scene = 2
    current_transaction.status = 1
    current_transaction.amount = bid.amount
    current_transaction.customer_name = datetime.now()
    current_transaction.mobile = bid.mobile
    current_transaction.bid_id = bid.id
    current_transaction.bid_contract_no = bid.contract_no
    current_transaction.payment_channel = "富友"
    current_transaction.payment_channel_id = 2
    current_transaction.event_id = event_id
    current_transaction.channel_id = bid.channel_id
    current_transaction.transaction_time = datetime.now()
    current_transaction.comment = None
    transaction_list = list()
    # 插入transaction记录初始化
    transaction_zero = get_transaction(contract_no, bid, event_id, 0)
    transaction_list.append(transaction_zero)
    # 插入transaction记录成功
    transaction = get_transaction(contract_no, bid, event_id, 1)
    transaction_list.append(transaction)
    convert.add_all(transaction_list)
    # 插入current_transaction记录
    convert.add_one(current_transaction)
    # 更新bid表
    convert.update_table(models.Bid, update, id=bid_id)
    # 更新bill表
    update_bill = {'status': 7}
    convert.update_table(models.Bill, update_bill, id=bid_id)
    return convert.add_one(bid_workflow)


# operate('1_0_15180279540_1550665419452', 9549969456)


def operate_overdue(event_id, bid_id, mark_overdue_time):
    """
    逾期还款 线上
    更新bid表、插入bid_workflow记录
    :return:
    """
    update = {'status': 7, 'repayment_time_type': 3, 'repayment_approach_type': 1, 'repayment_credit_type': 1}
    bid = convert.query(models.Bid, id=bid_id).first()
    contract_no = get_contract_no()
    # 插入bid_workflow记录
    bid_workflow = models.BidWorkflow()
    bid_workflow.id = my_snow().get_next_id()
    bid_workflow.company_id = bid.company_id
    bid_workflow.bid_id = bid.id
    bid_workflow.user_id = bid.user_id
    bid_workflow.last_status = 4
    bid_workflow.current_status = 7
    bid_workflow.operator_id = 0
    bid_workflow.operating_time = datetime.now()
    bid_workflow.action = "还款"
    bid_workflow.suggestion = None
    bid_workflow.channel_id = bid.channel_id
    # 插入current_transaction记录
    current_transaction = models.CurrentTransaction()
    current_transaction.id = my_snow().get_next_id()
    current_transaction.company_id = bid.company_id
    current_transaction.contract_no = contract_no
    current_transaction.type = 2
    current_transaction.scene = 2
    current_transaction.status = 1
    current_transaction.amount = bid.amount
    current_transaction.customer_name = datetime.now()
    current_transaction.mobile = bid.mobile
    current_transaction.bid_id = bid.id
    current_transaction.bid_contract_no = bid.contract_no
    current_transaction.payment_channel = "富友"
    current_transaction.payment_channel_id = 2
    current_transaction.event_id = event_id
    current_transaction.channel_id = bid.channel_id
    current_transaction.transaction_time = datetime.now()
    current_transaction.comment = None
    transaction_list = list()
    # 插入transaction记录初始化
    transaction_zero = get_transaction(contract_no, bid, event_id, 0)
    transaction_list.append(transaction_zero)
    # 插入transaction记录成功
    transaction = get_transaction(contract_no, bid, event_id, 1)
    transaction_list.append(transaction)
    convert.add_all(transaction_list)
    # 插入current_transaction记录
    convert.add_one(current_transaction)
    # 更新bid表
    convert.update_table(models.Bid, update, id=bid_id)
    # 更新bill表
    total_overdue_days = random.randint(0, 30)
    update_bill = {'status': 7, 'mark_overdue_time': mark_overdue_time, 'total_overdue_days': total_overdue_days}
    convert.update_table(models.Bill, update_bill, id=bid_id)
    return convert.add_one(bid_workflow)
