import time

# 序列号
sequence = 0
# 上一次时间戳
laststmp = -1


class MySnow:
    # 起始时间戳 2019-01-01 00:00:00
    __start_stmp = 1546272000
    # 序列号占用位数
    __sequence_bit = 12
    # user_id占用的位数
    # __user_bit = 17
    # 机器占用的占用的位数
    __machine_bit = 4
    # 每部分的最大值
    __max_sequence_num = -1 ^ (-1 << __sequence_bit)
    # __max_user_num = -1 ^ (-1 << __user_bit)
    __max_machine_num = -1 ^ (-1 << __machine_bit)
    # 每部分左移位数
    # __user_left = __sequence_bit + __machine_bit
    __timestmp_left = __sequence_bit + __machine_bit
    __machine_left = __sequence_bit

    # 机器码 读取配置文件
    machine = 0

    def __init__(self):
        pass

    def get_time(self):
        """
        获取时间戳
        :return: 返回时间戳
        """
        return int(time.time())

    def get_next_time(self):
        """
        获取下一次时间戳
        :return: 返回时间戳
        """
        global laststmp
        mill = self.get_time()
        while(mill <= laststmp):
            mill = self.get_time()
        return mill

    def get_next_id(self):
        """
        获取ID
        :return: 返回ID
        """
        global laststmp
        global sequence
        currStmp = self.get_time()
        if(currStmp < laststmp):
            raise NameError('Clock moved backwards.  Refusing to generate id')
        if(currStmp == laststmp):
            sequence = (sequence + 1) & self.__max_sequence_num
            if(sequence == 0):
                currStmp = self.get_next_time()
        else:
            sequence = 0
        laststmp = currStmp
        # 位运算生成id
        return (currStmp - self.__start_stmp) << self.__timestmp_left |\
               self.machine << self.__machine_left |sequence

