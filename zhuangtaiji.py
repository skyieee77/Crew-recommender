# -*- coding: UTF-8 -*-
import random
import random
import matplotlib.pyplot as plt
import time

class PumpStation:
    def __init__(self):
        self.units = ["12", "13", "23"]  # 机组组合
        self.current_unit = None
        self.schedule = []  # 排班表
        self.penalty_factors = {"12": 1.0, "13": 1.0, "23": 1.5}  # 惩罚因子
        self.unit_runtimes = {"12": 0, "13": 0, "23": 0}  # 记录机组运行时间

    def generate_schedule(self):
        # 生成两周的排班表，确保每两周更换一次机组组合
        for i in range(0, 14, 2):
            random.shuffle(self.units)  # 随机排序机组组合
            self.schedule.extend(self.units)

    def monitor_health(self, unit):
        # 模拟健康监测，返回True表示机组需要维修
        return random.choice([True, False])

    def select_unit(self):
        if not self.schedule:
            self.generate_schedule()

        next_unit = self.schedule.pop(0)

        # 基于惩罚因子选择机组
        if self.current_unit and next_unit != self.current_unit:
            if self.penalty_factors[next_unit] < self.penalty_factors[self.current_unit]:
                self.current_unit = next_unit
        else:
            self.current_unit = next_unit

        return self.current_unit

    def run_pump_station(self):
        plt.ion()  # 开启交互模式
        fig, ax = plt.subplots()

        while True:
            selected_unit = self.select_unit()
            print(f"Selected Unit: {selected_unit}")

            if self.monitor_health(selected_unit):
                print(f"Unit {selected_unit} needs maintenance. Switching to another unit.")
            else:
                print(f"Unit {selected_unit} is operating normally.")
                self.unit_runtimes[selected_unit] += 1  # 增加机组运行时间

            # 绘制机组运行时间
            ax.clear()
            ax.bar(self.unit_runtimes.keys(), self.unit_runtimes.values())
            ax.set_xlabel("Unit")
            ax.set_ylabel("Runtime (hours)")
            plt.pause(1)  # 暂停一秒钟以便观察图形

            # 模拟每两周更换一次机组组合
            if not self.schedule:
                print("Two weeks have passed. Generating a new schedule.")
                self.generate_schedule()

if __name__ == "__main__":
    pump_station = PumpStation()
    pump_station.run_pump_station()

# class PumpStation:
#     def __init__(self):
#         self.units = ["12", "13", "23"]  # 机组组合
#         self.current_unit = None
#         self.schedule = []  # 排班表
#         self.penalty_factors = {"12": 1.0, "13": 1.0, "23": 1.5}  # 惩罚因子
#
#     def generate_schedule(self):
#         # 生成两周的排班表，确保每两周更换一次机组组合
#         for i in range(0, 14, 2):
#             random.shuffle(self.units)  # 随机排序机组组合
#             self.schedule.extend(self.units)
#
#     def monitor_health(self, unit):
#         # 模拟健康监测，返回True表示机组需要维修
#         return random.choice([True, False])
#
#     def select_unit(self):
#         if not self.schedule:
#             self.generate_schedule()
#
#         next_unit = self.schedule.pop(0)
#
#         # 基于惩罚因子选择机组
#         if self.current_unit and next_unit != self.current_unit:
#             if self.penalty_factors[next_unit] < self.penalty_factors[self.current_unit]:
#                 self.current_unit = next_unit
#         else:
#             self.current_unit = next_unit
#
#         return self.current_unit
#
#     def run_pump_station(self):
#         while True:
#             selected_unit = self.select_unit()
#             print(f"Selected Unit: {selected_unit}")
#
#             if self.monitor_health(selected_unit):
#                 print(f"Unit {selected_unit} needs maintenance. Switching to another unit.")
#             else:
#                 print(f"Unit {selected_unit} is operating normally.")
#
#             # 模拟每两周更换一次机组组合
#             if not self.schedule:
#                 print("Two weeks have passed. Generating a new schedule.")
#                 self.generate_schedule()
#
# if __name__ == "__main__":
#     pump_station = PumpStation()
#     pump_station.run_pump_station()
