#!/user/bin/python3
# @Author:  LSY
# @Date:    2019/2/21

task_headers = {"Content-Type": "application/json;charset=UTF-8"
    , "X-Moxie-Event": "bill"
    , "X-Moxie-Type": "carrier"
    , "X-Moxie-Signature": "lHEudlATi7NfuUl9HYBi1QER1s6RSGHc7EV3IPxXsk8="
    , "X-Moxie-Uid": "c31b3f75-6cab-445f-b4ba-1a9b8797477c"}

report_headers = {"Content-Type": "application/json;charset=UTF-8"
    , "X-Moxie-Event": "bill"
    , "X-Moxie-Type": "carrier"
    , "X-Moxie-Signature": "70YFW6bVxmlpkRCa83T9GqgsxTga6M0Hf2odD7z06DE="
    , "X-Moxie-Uid": "c31b3f75-6cab-445f-b4ba-1a9b8797477c"}

bill_headers = {"Content-Type": "application/json;charset=UTF-8"
    , "X-Moxie-Event": "bill"
    , "X-Moxie-Type": "carrier"
    , "X-Moxie-Signature": "OWIVNHuLxuNETzjj8wLBDGJb5s6ZMXJLQp1RHr5ohUA="
    , "X-Moxie-Uid": "c31b3f75-6cab-445f-b4ba-1a9b8797477c"}

task_data = '{"mobile":"13252997321","timestamp":1551086897550,"result":true,"message":"登录成功","user_id":"200_528_13252997321_1551086486841","task_id":"a1e06150-38df-11e9-968a-00163e0d2629"}'
bill_data = '{"mobile":"13252997321","user_id":"200_528_13252997321_1551086486841","task_id":"a1e06150-38df-11e9-968a-00163e0d2629","bills":["2019-02","2019-01","2018-12","2018-11","2018-10","2018-09"]}'
report_data = '{"mobile":"13252997321","name":"潘亮","idcard":"210212198403275917","timestamp":1551087113301,"result":true,"message":"aX92rOy5T07a5%2B05tXXYwPAxxpw168u7E41Ob4fHTWnFbkNpSYQGsU2iHY2qhfLvZEdOzKP4JBmP1tusSr3QH2XQ17ykDyyJ3dE7OowxxSh0Yyp7Z6N%2Bjyl4xfbPBSBBkhI9WyoxJomxclOjX1H0axTRFIahSUKdTv05HGLu4YFi9kgZLiWfjFy%2BiwaThFyZ","task_id":"a1e06150-38df-11e9-968a-00163e0d2629","user_id":"200_528_13252997321_1551086486841"}'