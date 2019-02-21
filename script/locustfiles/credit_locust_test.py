import sys, os

sys.path.append(os.getcwd())
import threading
import time
from script.credit.moxie_data import data
from script.credit.youdun_data import get_youdun_recognization
from locust import HttpLocust, TaskSequence, task, seq_task
from script.credit.moxie_callback_data import data as moxie_callback_data, headers as moxie_callback_headers
from script.credit.sdk_data import data as sdk_callback_data
from script.credit.youdun_callback_data import youdun_callback_data
import json
counter = 0


class WebsiteTasks(TaskSequence):
    @seq_task(1)  # 任务执行的顺序
    @task(1)  # 任务执行的比重
    def get_event_id(self):
        """
        初始化event_id
        :return:
        """
        print("start gene event_id")

        company_id = "1"
        channel_id = "0"
        mobile = 13700000000 + self.locust.get_count()
        timestamp = int(round(time.time() * 1000))
        self.event_id = company_id + "_" + channel_id + "_" + str(mobile) + "_" + str(timestamp)

    @seq_task(2)
    @task(1)
    def moxie_carrier(self):
        """
        模拟魔蝎运营商数据请求
        :return:
        """
        print("moxie carrier request")

        payload = dict(eventId=self.event_id, result=data)
        self.client.post("/", payload)

    @seq_task(3)
    @task(1)
    def youdun_recognize(self):
        """
        模拟有盾回调
        :return:
        """
        result = get_youdun_recognization()

        payload = dict(eventId=self.event_id, result=result)
        self.client.post('/youdun/recognize', data=payload)

    @seq_task(4)
    @task(1)
    def moxie_callback(self):
        """
        模拟魔蝎回调
        :return:
        """
        event_id = self.event_id
        try:
            response = self.client.post('/callback/moxie-carrier/bill', data=moxie_callback_data,
                                        headers=moxie_callback_headers)
            if response.status_code == 201:
                print("魔蝎回调成功.event_id: %s" % event_id)
            else:
                print("魔蝎回调失败.event_id: %s" % event_id)
        except Exception as e:
            print("魔蝎回调失败.event_id: %s" % event_id)

    @seq_task(5)
    @task
    def sdk_callback(self):
        """
        模拟sdk上传数据
        :return:
        """
        event_id = self.event_id
        payload = dict(eventId=event_id, data=sdk_callback_data)
        try:
            response = self.client.post('/sdk/saveData', data=payload)
            if response.status_code == 200:
                print("sdk数据上传成功。event_id: %s" % event_id)
        except Exception as e:
            print("sdk上传数据失败，exception: %s" % e)

    @seq_task(6)
    @task
    def youdun_recognize_callback(self):
        """
        模拟有盾活体检测回调
        :return:
        """
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        data = json.loads(youdun_callback_data)
        event_id = self.event_id
        try:
            response = self.client.post('/callback/youdun/recognition', data=json.dumps(data),
                                        headers=headers)
            response_data = json.loads(response.content)
            if response_data['code'] == '1':
                print("有盾活体检测回调成功。event_id: %s" % event_id)
            else:
                print("有盾回调失败。event_id: %s" % event_id)
        except Exception as e:
            print("有盾回调失败。event_id: %s, exception: %s" % (event_id, e))


class WebUserLocust(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 100
    max_wait = 200
    host = 'http://localhost:20997/rum/test'

    def get_count(self):
        """
        原子操作,获取计数值
        :return:
        """
        global counter
        threadLock = threading.Lock()
        with threadLock:
            counter += 1

        return counter