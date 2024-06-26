# -*- coding: UTF-8 -*-
import random

class PumpStation:
    def __init__(self):
        self.units = ["12", "13", "14", "23", "24", "34"]  # 机组组合
        self.current_units = ["12", "13", "14", "23"]  # 初始机组组合，1、2、3、4号机组
        self.schedule = []  # 排班表
        self.penalty_factors = {
            "<2000": "Unknow",
            "2000-2600": {"34": 1.5, "12": 1.2},
            "2600-3300": {"12": 1.5, "24": 1.3},
            "3300-3800": {"14": 1.5, "24": 1.3},
            ">3800": "Unknow"
        }  # 惩罚因子
        self.operating_hours = {unit: 0 for unit in self.units}  # 机组运行时间记录

    def generate_schedule(self):
        # 生成30周的排班表，确保每两周更换一次机组组合
        for i in range(0, 30, 2):
            random.shuffle(self.current_units)  # 随机排序机组组合
            self.schedule.extend(self.current_units)

    def select_unit(self, week):
        if not self.schedule:
            self.generate_schedule()

        next_unit = self.schedule.pop(0)

        if week % 2 == 0:
            # 每两周检查一次是否需要更换机组组合
            if self.should_change_combination():
                self.change_combination()

        return next_unit

    def should_change_combination(self):
        # 检查是否需要更换机组组合
        total_hours = sum(self.operating_hours[unit] for unit in self.current_units)
        return total_hours > 0 and total_hours % 60 == 0  # 模拟每两周更换一次

    def change_combination(self):
        # 更换机组组合
        new_combination = random.choice(self.units)
        self.current_units = self.current_units[:4] + [new_combination]

    def run_pump_station(self):
        for week in range(1, 31):
            selected_unit = self.select_unit(week)
            self.operating_hours[selected_unit] += 1
            if week % 2 == 0:
                print(f"Week {week-1} and {week}: Selected Unit: {selected_unit}")

    def calculate_penalty(self):
        penalty_hours = {unit: 0 for unit in self.units}
        for unit, hours in self.operating_hours.items():
            if unit not in self.penalty_factors:
                continue
            for range_str, factor_dict in self.penalty_factors[unit].items():
                lower, upper = map(int, range_str.split("-"))
                if lower <= hours <= upper:
                    penalty_hours[unit] += 1
        return penalty_hours

if __name__ == "__main__":
    pump_station = PumpStation()
    pump_station.run_pump_station()
    penalty_hours = pump_station.calculate_penalty()
    print("\nOperating Hours:")
    for unit, hours in pump_station.operating_hours.items():
        print(f"Unit {unit}: {hours} hours")
    print("\nPenalty Hours:")
    for unit, hours in penalty_hours.items():
        print(f"Unit {unit}: {hours} hours")
