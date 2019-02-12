import sys, os

sys.path.append(os.getcwd())
import threading
import time
from script.credit.moxie_data import data
from script.credit.youdun_data import get_youdun_recognization
from locust import HttpLocust, TaskSequence, task, seq_task

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
        self.client.post("/rum/test/", payload)

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


class WebUserLocust(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 100
    max_wait = 200
    host = 'http://localhost:20997'

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
