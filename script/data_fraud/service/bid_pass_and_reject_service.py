from utils import convert, models
from datetime import datetime
from utils.my_snowflake import my_snow
import requests
from config import constant
import json

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

def sake_login(user,password):
    """
    
    :param user: 用户名
    :param password: 密码
    :return: 
    """
    login_req_body = dict(account=str(user), password=str(password))
    login_response = requests.post(url=constant.SAKE_BASE_URL_STAGING + '/management/login', data=login_req_body)
    login_response_header = login_response.headers

    if login_response.status_code != 200:
        login_response.failure("login failed, account: ", user)
    else:
        authorization = login_response_header["Authorization"]
        print("get Authorization response: ", authorization)


    return authorization


def loan_audit_success(event_id, user='admin', password='admin', comment=''):
    """
    审核通过
    :param event_id: 事件ID
    :param authorization: 验签
    :return:
    """
    authorization =sake_login(user,password)
    event = convert.query(models.Event,event_id=event_id).first()
    bid_id = event.bid_id
    if bid_id is None:
        print("no bidId")
    granting_loan_body = dict(bidId = str(bid_id),comment = str(comment))
    headers={"Authorization":authorization}
    granting_loan = requests.post(url = constant.SAKE_BASE_URL_STAGING+ '/supervisor/granting/loans/pass',data=granting_loan_body,headers=headers)
    if granting_loan.status_code != 200:
        print("granting failed, bidId: ", bid_id)
    else:
        print("granting success ")
    fuyou_data = dict(eventId = event_id)
    fuyou_loan_result = requests.post(constant.RUM_BASE_URL_STAGING+'/fuioucallback/data/fraud/success',data=fuyou_data)
    if fuyou_loan_result.status_code != 200:
        print("loan false: ", event_id)
    else:
        print("loan success ")


def loan_audit_false(event_id, user='admin', password='admin', comment=''):
    """
    审核拒件
    :param event_id: 事件ID
    :param authorization: 验签
    :return:
    """
    authorization =sake_login(user,password)
    event = convert.query(models.Event,event_id=event_id).first()
    bid_id = event.bid_id
    if bid_id is None:
        print("no bidId")
    granting_loan_body = dict(bidId = str(bid_id),comment = str(comment))
    headers={"Authorization":authorization}
    granting_loan = requests.post(url = constant.SAKE_BASE_URL_STAGING+ '/supervisor/granting/loans/reject',data=granting_loan_body,headers=headers)
    if granting_loan.status_code != 200:
        print("granting failed, bidId: ", bid_id)
    else:
        print("granting reject ")


def repayment(event_id,token):
    """
    还款成功
    :param event_id: 事件ID
    :param token:验签
    :return:
    """
    event = convert.query(models.Event,event_id=event_id).first()
    bid_id = event.bid_id
    bid = convert.query(models.Bid,id=bid_id).first()
    mobile = bid.mobile
    company_id = bid.company_id
    channel_id = bid.channel_id
    bank_account_id = bid.bank_account_id
    bill = convert.query(models.Bill,bid_id = bid_id,is_deleted='0').first()
    repayment_amout = bill.repayment_amount
    extension_repayment = 'false'
    headers = {"Token":token}
    sms_data = dict(mobile = str(mobile),companyId= str(company_id),channelId = str(channel_id),eventId = str(event_id),bidId = str(bid_id),bankAccountId = str(bank_account_id),repaymentAmount=str(repayment_amout))
    sms_result = requests.post(constant.ICEWINE_BASE_URL_STAGING+'/repayment/sms',data = sms_data,headers=headers)
    if sms_result.status_code != 200:
        print("sms failed, bidId: ", bid_id)
    else:
        print("sms reject ")
    vcode = '0123'
    repayment_data = dict(mobile = str(mobile),companyId= str(company_id),channelId = str(channel_id),eventId = str(event_id),bidId = str(bid_id),bankAccountId = str(bank_account_id),repaymentAmount=str(repayment_amout),vcode=vcode,extensionRepayment=extension_repayment)
    repayment_result = requests.post(constant.ICEWINE_BASE_URL_STAGING+'/repayment/online',data = repayment_data,headers = headers)
    if repayment_result.status_code != 200:
        print("repayment failed, bidId: ", bid_id)
    else:
        print("repayment reject ")
    third_party_event_data = dict(eventId=str(event_id),companyId=str(company_id),channelId=str(channel_id),mobile=str(mobile),timestamp=str(int(datetime.now().timestamp()*1000)),type='2',scene = "2",status ="1",amount=str(repayment_amout),contractNo=str(bid.contract_no),paymentChannelName="富有",paymentChannelId="2",updateTime=datetime.now().time().strftime("%Y-%m-%d %H:%M:%S"))
    third_party_event_result = requests.post(constant.SAKE_BASE_URL_LOCAL+"/test/repayment",data = third_party_event_data)
    if third_party_event_result.status_code != 200:
        print("third_party_event, bidId: ", bid_id)
    else:
        print("repayment success ")


if __name__ == '__main__':
    account = 'admin'
    password = 'admin'
    event_id = "200_0_15798405328_1556524087424"
    loan_audit_success(event_id,account,password)
    print("111")
    # event_id = '200_0_14579578024_1556515363222'
    # token = '013f3e0b626303655395efbdacc929ba171a746322b14f5be93d3b61dbd06c91'
    # repayment(event_id,token)
