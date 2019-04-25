# -*- coding: utf-8 -*-
from script.demo.util.UserUtil import bid_application_insert
from script.demo.util.UserUtil import register_insert
from script.service.autonym_service import request_profile_validation
from script.service.user_certification_service import insert_operator, insert_bankcard

if __name__ == '__main__':
    # # 初始化数据
    company_id = 200
    channel_id = 0
    gmt_create = "2019-04-25 17:39:25"
    mobile_platform = 1
    # 完成插入uer、user_detail表数据
    register_dict = register_insert(company_id, channel_id, gmt_create, mobile_platform)

    # 需要经过各种认证进行以上两表的数据补全
    # 实名制认证
    event_id = register_dict.get("event_id")
    mobile = register_dict.get("mobile")
    token = register_dict.get("token")
    request_profile_validation(company_id, channel_id, event_id, mobile, token)
    # 运营商认证
    insert_operator(mobile, company_id)
    # 银行卡认证
    insert_bankcard(mobile, company_id)
    # 申请进件
    bid_application_insert(company_id, channel_id, mobile, token, event_id)
