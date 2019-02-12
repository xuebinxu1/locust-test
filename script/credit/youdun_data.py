from . import image_generator

__data={
  "creation_time": "20190118100946",
  "birthday": "1995.01.20",
  "classify": "2",
  "id_number": "331021199501201274",
  "address": "杭州市下城区东新路155号",
  "gender": "男",
  "nation": "汉",
  "idcard_portrait_photo": "",
  "auth_result": "T",
  "validity_period": "2017.12.27-2027.12.27",
  "sign": "041FB5BCA3813F3B910EE880D38C1809",
  "risk_tag": {
    "living_attack": "0"
  },
  "id_name": "黄家豪",
  "idcard_front_photo": "",
  "sign_time": "20190118101008",
  "partner_order_id": "11111",
  "result_status": "01",
  "similarity": "0.9562",
  "idcard_back_photo": "",
  "issuing_authority": "杭州市公安局下城分局",
  "living_photo": "",
  "verify_status": "1",
  "partner_code": "201901092871387003",
  "age": "23"
}

def get_youdun_recognization():
    __data['portrait'] = image_generator.get_image_base64('上半身')
    __data['idcard_front_photo'] = image_generator.get_image_base64('正面')
    __data['idcard_back_photo'] = image_generator.get_image_base64("背面")
    __data['living_photo'] = image_generator.get_image_base64('活体')

    return __data