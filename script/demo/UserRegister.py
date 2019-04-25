# -*- coding: utf-8 -*-
# from script.demo.util.UserUtil import vcode, login, carrier
from script.demo.util.UserUtil import carrier, register

if __name__ == '__main__':
    # 完成插入uer、user_detail表数据
    # vcode_dict = vcode()
    # mobile = vcode_dict.get("mobile")
    # company_id = vcode_dict.get("company_id")
    # channel_id = vcode_dict.get("channel_id")
    # event_id = vcode_dict.get("event_id")
    # mobile_platform = vcode_dict.get("mobile_platform")
    # token = login(mobile, company_id, channel_id, mobile_platform, event_id)
    # 需要经过各种认证进行以上两表的数据补全
    # 进行运营商认证
    # carrier("b09e1e8ce2f3484cf889dc0fd18fa31bb6e38410e74d26eb4470e6b68f756955", 200, 0, 18182346296,
    #         "200_0_18182346296_1556162675130")
    register(200,0)
