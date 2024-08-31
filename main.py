import numpy as np
import matplotlib.pyplot as plt
from world import World
from people import People
from elevator import Elevator


def draw(mean_value, std_value, note: str):
    plt.figure(figsize=(6, 6))
    plt.subplot(2, 1, 1)
    plt.bar(range(3, World.FLOORS + 1), mean_value)
    plt.xticks(range(3, World.FLOORS + 1))
    plt.title(f"mean {note}")
    plt.xlabel("floor")
    plt.ylabel("mean time(/Simulate time units)")

    plt.subplot(2, 1, 2)
    plt.title(f"std {note}")
    plt.bar(range(3, World.FLOORS + 1), std_value)
    plt.xticks(range(3, World.FLOORS + 1))
    plt.xlabel("floor")
    plt.ylabel("std")
    plt.tight_layout()
    plt.show()



if __name__ == '__main__':

    elevator_pool = [Elevator() for _ in range(World.NUM_ELEVATORS)]
    for time in range(World.SIMULATION_TIME):
        # 生成一个人
        if np.random.rand() < World.generate_query_rate:
            p = People()
            p.go_lunch()
            World.waiting_people.append(p)
            World.world_people.append(p)

        for people in World.waiting_people:
            print(f"people{people.id} 在{people.current_floor}楼等待, 目标楼层为{people.destination}")

        for elevator in elevator_pool:
            elevator.run()

        for elevator in elevator_pool:
            print(
                f"电梯{elevator.id}目前在{elevator.current_floor}楼, 电梯里面有{len(elevator.passengers)}个人, 电梯状态为{elevator.state}")

        print("==============\n")

        for people in World.waiting_people:
            people.waiting_time += 1

    print("模拟结束！！！")
    print(f"一共有{len(World.world_people)}个人乘坐电梯")
    print(f"一共有{len(World.waiting_people)}个人还没坐上电梯")

    waiting_time = [[] for _ in range(World.FLOORS + 1)]
    travel_time = [[] for _ in range(World.FLOORS + 1)]
    total_time = [[] for _ in range(World.FLOORS + 1)]
    for people in World.world_people:
        waiting_time[people.current_floor].append(people.waiting_time)
        travel_time[people.current_floor].append(people.travel_time)
        total_time[people.current_floor].append(people.waiting_time + people.travel_time)

    mean_waiting_time_each_floor = [np.mean(waiting_time[i]) for i in range(3, World.FLOORS + 1)]
    std_waiting_time_each_floor = [np.std(waiting_time[i], ddof=1) for i in range(3, World.FLOORS + 1)]
    mean_travel_time_each_floor = [np.mean(travel_time[i]) for i in range(3, World.FLOORS + 1)]
    std_travel_time_each_floor = [np.std(travel_time[i], ddof=1) for i in range(3, World.FLOORS + 1)]  # ddof=1表示除以n-1, 无偏估计
    mean_total_time_each_floor = [np.mean(total_time[i]) for i in range(3, World.FLOORS + 1)]
    std_total_time_each_floor = [np.std(total_time[i], ddof=1) for i in range(3, World.FLOORS + 1)]


    # 找一下哪个人等待的时间最长，他的轨迹是什么
    max_waiting_people = None
    for people in World.world_people:
        if not max_waiting_people:
            max_waiting_people = people
        if people.waiting_time > max_waiting_people.waiting_time:
            max_waiting_people = people

    print(f"等待时间最长的人是people{max_waiting_people.id}, 他的等待时间是{max_waiting_people.waiting_time}")
    print(f"他的路径是：{max_waiting_people.current_floor} -> {max_waiting_people.destination}")

    draw(mean_waiting_time_each_floor, std_waiting_time_each_floor, "waiting time")
    # draw(mean_travel_time_each_floor, std_travel_time_each_floor, "travel time")
    draw(mean_total_time_each_floor, std_total_time_each_floor, "total time")