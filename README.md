位于根目录执行

```
locust -f script/locustfiles/credit_locust_test.py

```


创建虚拟环境,并安装依赖

```
virtualenv --no-site-packages venv
source venv/bin/activate
pip3 install -f requirement.txt

```