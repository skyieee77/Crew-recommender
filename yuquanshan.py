# -*- coding: UTF-8 -*-
import random

class PumpStation:
    def __init__(self):
        self.large_units = ["12", "13", "23"]
        self.small_units = ["14", "15", "24", "25", "34", "35"]
        self.current_units = self.large_units  # 初始使用大机组
        self.schedule = []  # 排班表
        self.operating_hours = {unit: 0 for unit in self.large_units + self.small_units}  # 机组运行时间记录
        self.penalty_factors = {
            "<2300": "Unknow",
            "2300-3400": {"13": 1.2},
            "3400-5500": {},
            "5500-6500": {"25": 1.3, "35": 1.5, "24": 1.2, "14": 1.1},
            ">6500": {}
        }  # 惩罚因子

    def generate_schedule(self):
        # 生成20周的排班表
        for i in range(20):
            random.shuffle(self.current_units)  # 随机排序机组组合
            self.schedule.extend(self.current_units)

    def select_unit(self, week, flow_rate):
        if not self.schedule:
            self.generate_schedule()

        next_unit = self.schedule.pop(0)

        if week % 2 == 0:
            # 每两周检查一次是否需要更换机组组合
            if self.should_change_combination(flow_rate):
                self.change_combination()

        return next_unit

    def should_change_combination(self, flow_rate):
        # 检查是否需要更换机组组合
        total_hours = sum(self.operating_hours[unit] for unit in self.current_units)
        return total_hours > 0 and total_hours % 60 == 0 and flow_rate < 7000

    def change_combination(self):
        # 更换机组组合，根据流量选择大机组或小机组
        if random.random() < 0.5:
            self.current_units = self.large_units
        else:
            self.current_units = self.small_units

    def run_pump_station(self):
        flow_rates = []
        for week in range(1, 21):
            flow_rate = int(input(f"Week {week * 2 - 1} and {week * 2}: Enter flow rate: "))
            flow_rates.append(flow_rate)
            selected_unit = self.select_unit(week, flow_rate)
            self.operating_hours[selected_unit] += 1
            print(f"Week {week * 2 - 1} and {week * 2}: Selected Unit: {selected_unit}")

        return flow_rates

    def calculate_total_hours(self):
        total_hours = {unit: 0 for unit in self.large_units + self.small_units}
        for unit, hours in self.operating_hours.items():
            total_hours[unit] += hours
        return total_hours

if __name__ == "__main__":
    pump_station = PumpStation()
    flow_rates = pump_station.run_pump_station()
    total_hours = pump_station.calculate_total_hours()
    print("\nOperating Hours:")
    for unit, hours in total_hours.items():
        print(f"Unit {unit}: {hours} hours")
