import numpy as np
from world import World

class People:
    id = 1

    def __init__(self):
        self.id = People.id
        People.id += 1

        self.weight = np.random.randn() * 16 + 60  # 设定人的体重的均值为60kg，方差为16
        self.current_floor = World.random_choose_floor()
        self.destination = None
        self.waiting_time = 0
        self.travel_time = 0

    def __str__(self):
        return f"people{self.id} from {self.current_floor} to {self.destination}"

    @property
    def direction(self) -> str:
        return 'up' if self.destination > self.current_floor else 'down'

    def go_lunch(self):
        """
        去吃饭
        :return:
        """
        while self.current_floor in [1, 2]:  # 1楼和2楼，自己走下去了，不坐电梯
            self.current_floor = World.random_choose_floor()  # current_floor不在1楼和2楼

        # 随机选择目标楼层，目标楼层不能与当前楼层相同
        self.choose_destination()
        while self.current_floor == self.destination:
            self.choose_destination()

    def choose_destination(self):
        """
        选择目标楼层
        :return:
        """
        if World.LUNCH:
            if self.current_floor == 1:
                self.destination = World.random_choose_floor()
            else:
                self.destination = 1 if np.random.rand() < World.GOTO_LUNCH_RATE else World.random_choose_floor()
        else:
            raise "该去吃饭🍚了"
