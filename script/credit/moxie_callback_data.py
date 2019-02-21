#!/user/bin/python3
# @Author:  LSY
# @Date:    2019/2/21

headers = {"Content-Type": "application/json;charset=UTF-8"
    , "X-Moxie-Event": "bill"
    , "X-Moxie-Type": "carrier"
    , "X-Moxie-Signature": "cXc4nB7JGH1wse1QOWZ9Hbfa/V5XldYtaQM4LW79K2U="
    , "X-Moxie-Uid": "c31b3f75-6cab-445f-b4ba-1a9b8797477c"}

data = '{"mobile":"15180279540","user_id":"1_0_15180279540_1550665419452","task_id":"4cb9e910-350d-11e9-89a0-00163e0f4efb","bills":["2019-02","2019-01","2018-12","2018-11","2018-10","2018-09"]}'