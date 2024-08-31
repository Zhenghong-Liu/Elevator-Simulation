import numpy as np


class World:
    TICK = 1  # 模拟的时间间隔， 单位可以认为是秒
    NUM_ELEVATORS = 3  # 电梯的数量
    FLOORS = 20  # 大楼的楼层数
    SIMULATION_TIME = 10000  # Time steps

    LUNCH = True  # 午餐时间， 大家都准备去吃饭，目标楼层大多数都是1楼
    GOTO_LUNCH_RATE = 0.9
    generate_query_rate = 0.9132523  # 生成一个坐电梯请求的概率

    # TO_OFFICE = False  # 午餐时间后， 大家都准备回办公室，目标楼层大多数自己所在的楼层

    waiting_people = []  # 等待乘坐电梯的人
    world_people = []  # 这个模拟过程中生成的所有人

    @staticmethod
    def random_choose_floor():
        """
        随机去一个楼层
        :return:
        """
        return np.random.randint(1, World.FLOORS + 1)
