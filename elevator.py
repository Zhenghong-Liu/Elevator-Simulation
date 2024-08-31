"""
电梯类
想要模拟一下，如果大家都去吃饭，那么哪个楼层的等待时间最长
"""

from world import World


class Elevator:
    id = 1

    def __init__(self):
        self.id = Elevator.id
        Elevator.id += 1

        self.capacity = 1000  # 电梯最大承载量, 默认为1000kg
        self.current_floor = 1  # 当前楼层, 默认为1楼
        self.direction = None  # 电梯运行方向, 默认为上行， up: 上行, down: 下行， none表示电梯里面没人，没有人要坐电梯
        self.passengers = []  # 电梯里面的乘客
        self.destination = None  # 电梯准备要去哪个楼层
        # self.moving = False  # 电梯是否在运行
        self.state = 0  # 0表示开门， 1表示关门， 2表示运行  开门需要耗时1秒， 关门需要耗时1秒， 运行需要耗时1秒
        self.weight = 0  # 电梯当前的重量

    def query_people_need_down(self) -> bool:
        """
        判断电梯是否需要有人下电梯
        :return:
        """
        return any(p.destination == self.current_floor for p in self.passengers)

    def query_people_need_up(self) -> bool:
        """
        判断电梯是否需要有人上电梯
        :return:
        """
        for people in World.waiting_people:
            if people.current_floor == self.current_floor and self.weight <= self.capacity - 60 and self.direction == people.direction:
                return True
        return False

    def people_out(self):
        """
        有人下电梯
        :return:
        """
        # 如果到地方了，就输出这个人的路径
        for people in self.passengers:
            if people.direction == self.current_floor:
                print(people)

        self.passengers = [p for p in self.passengers if p.destination != self.current_floor]
        self.weight = sum(p.weight for p in self.passengers)

    def people_in(self):
        """
        有人上电梯
        :return:
        """
        for people in World.waiting_people:
            if people.current_floor == self.current_floor and self.weight + people.weight <= self.capacity:
                if not self.passengers or self.direction == people.direction:
                    self.direction = people.direction
                    self.passengers.append(people)
                    World.waiting_people.remove(people)
                    self.weight += people.weight

    def people_travel(self):
        """
        有人在电梯里面
        :return:
        """
        for people in self.passengers:
            people.travel_time += 1

    def update_direction(self):
        """
        更新电梯的运行方向
        :return:
        """
        if not self.passengers:  # 如果电梯是空的，去接人(可能是电梯本来就没人，也可能是人在某个楼层下完了，空了)
            if not World.waiting_people:  # 如果没人在等电梯，那么电梯不动
                self.direction = None
                return

            if self.direction == "up":
                # 现在是电梯里面没有人，然后有人等待，电梯之前是向上走的
                if any(p.current_floor > self.current_floor for p in World.waiting_people):
                    self.direction = "up"
                else:
                    self.direction = None
            elif self.direction == "down":
                # 现在是电梯里面没有人，然后有人等待，电梯之前是向下走的
                if any(p.current_floor < self.current_floor for p in World.waiting_people):
                    self.direction = "down"
                else:
                    self.direction = None
            else:
                # 电梯里面没有人，然后有人等待，电梯之前没有运行
                if any(p.current_floor > self.current_floor for p in World.waiting_people):
                    self.direction = "up"
                else:
                    self.direction = "down"
        else:
            self.direction = self.passengers[0].direction

    def run(self):
        """
        电梯运行
        :return:
        """
        self.people_travel()
        self.update_direction()

        if self.state == 0:
            self.people_out()
            self.people_in()
            self.state = 1
            return
        elif self.state == 1:
            self.state = 2
        elif self.state == 2:
            if self.query_people_need_up() or self.query_people_need_down():
                self.state = 0
                return

            # 将电梯移动到下一个楼层
            if self.direction == 'up':
                if self.current_floor == World.FLOORS + 1:
                    self.direction = None
                else:
                    self.current_floor += 1
            elif self.direction == 'down':
                if self.current_floor == 0:
                    self.direction = None
                else:
                    self.current_floor -= 1
            else:
                return  # 电梯不动




