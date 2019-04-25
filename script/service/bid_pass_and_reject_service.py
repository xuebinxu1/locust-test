from utils import convert, models
from datetime import datetime
from utils.my_snowflake import my_snow


def bid_pass(bid_id):
    """
    审核通过
    更新bid表、插入bid_workflow记录
    :return:
    """
    update = {'status': 2}  # 2 发放贷款(待放款),下一个阶段会通过放款成功进入还款(待还款)阶段
    bid = convert.query(models.Bid, id=bid_id).first()
    bid_workflow = models.BidWorkflow()
    bid_workflow.id = my_snow().get_next_id()
    bid_workflow.company_id = bid.company_id
    bid_workflow.bid_id = bid.id
    bid_workflow.user_id = bid.user_id
    bid_workflow.last_status = 1
    bid_workflow.current_status = 2
    bid_workflow.operator_id = 0
    bid_workflow.operating_time = datetime.now()
    bid_workflow.action = "调用规则进件"
    bid_workflow.suggestion = None
    bid_workflow.channel_id = bid.channel_id
    # 更新bid表
    convert.update_table(models.Bid, update, id=bid_id)
    return convert.add_one(bid_workflow)


# bid_pass(9549969456)


def bid_reject(event_id, bid_id):
    """
    拒件
    更新bid表、event表
    插入bid_workflow记录
    :return:
    """
    update = {'status': 6}  # 拒件
    update_event = {'is_expired': 1}
    bid = convert.query(models.Bid, id=bid_id).first()
    bid_workflow = models.BidWorkflow()
    bid_workflow.id = my_snow().get_next_id()
    bid_workflow.company_id = bid.company_id
    bid_workflow.bid_id = bid.id
    bid_workflow.user_id = bid.user_id
    bid_workflow.last_status = 0
    bid_workflow.current_status = 6
    bid_workflow.operator_id = 0
    bid_workflow.operating_time = datetime.now()
    bid_workflow.action = "调用规则进件"
    bid_workflow.suggestion = None
    bid_workflow.channel_id = bid.channel_id
    # 更新event表
    convert.update_table(models.Event, update_event, event_id=event_id)
    # 更新bid表
    convert.update_table(models.Bid, update, id=bid_id)
    return convert.add_one(bid_workflow)

# bid_reject('1_0_15180279540_1550665419452', 9549969456)
