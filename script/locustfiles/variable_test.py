import sys, os

sys.path.append(os.getcwd())
import threading
import time
import random
import hashlib
import json
import config.constant as constant
from script.credit.vodka_request import data as vodka_data
from locust import HttpLocust, TaskSequence, task, seq_task


class WebsiteTasks(TaskSequence):
    @seq_task(1)  # 任务执行的顺序
    @task(1)  # 任务执行的比重
    def vcode(self):
        data = json.loads(vodka_data)
        header = {"Content-Type": "application/json"}
        # self.client.headers.update(header)
        response = self.client.post('/vodka/variable/compute', data=json.dumps(data), headers=header)
        print(json.loads(response.content))
        pass


class WebUserLocust(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 1000
    max_wait = 2000
    host = 'http://192.168.31.40:20787'

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

