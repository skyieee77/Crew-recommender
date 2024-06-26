# -*- coding: UTF-8 -*-
import random


class Unit:
    def __init__(self, unit_id):
        self.unit_id = unit_id
        self.sub_units = [int(digit) for digit in str(unit_id)]
        self.total_runtime = 0
        self.efficiency = efficiency_factors[unit_id]
        self.health_coefficient = health_factors[unit_id]
        self.record = ""

    def add_runtime(self, hours):
        # 考虑节能系数和健康系数
        self.total_runtime += hours * self.efficiency * self.health_coefficient
        for sub_unit in self.sub_units:
            if sub_unit in sub_unit_runtimes:
                sub_unit_runtimes[sub_unit] += hours * self.efficiency * self.health_coefficient
                sub_unit_record[sub_unit] += " + " + str(hours) + "*" + str(self.efficiency) + "*" + str(self.health_coefficient)
            else:
                sub_unit_runtimes[sub_unit] = hours * self.efficiency * self.health_coefficient
                sub_unit_record[sub_unit] = str(hours) + "*" + str(self.efficiency) + "*" + str(self.health_coefficient)


# 定义状态机状态枚举
class UnitState:
    SMALL = "Small"
    LARGE = "Large"


# 定义状态机类
class PumpStationStateMachine:
    def __init__(self, units):
        self.current_state = UnitState.SMALL  # 初始状态为小机组
        self.units = units  # 机组列表
        self.weeks_elapsed = 0
        self.last_unit = None

    def switch_to_small_unit(self):
        # 切换到小机组状态
        self.current_state = UnitState.SMALL
        self.weeks_elapsed = 0

    def switch_to_large_unit(self):
        # 切换到大机组状态
        self.current_state = UnitState.LARGE
        self.weeks_elapsed = 0

    def select_unit(self, water_flow):
        self.weeks_elapsed += 1

        if self.current_state == UnitState.SMALL:
            if self.weeks_elapsed >= 2:
                # 每两周切换一次
                self.switch_to_large_unit()
        elif self.current_state == UnitState.LARGE:
            if self.weeks_elapsed >= 2:
                # 每两周切换一次
                self.switch_to_small_unit()

        # 根据水量和上次开机机组选择下一个机组
        if water_flow >= 7000:
            # 使用大机组
            eligible_units = [(unit, efficiency_factors[unit.unit_id]) for unit in self.units if
                              unit.unit_id in [12, 13, 23] and unit != self.last_unit]
        else:
            # 使用小机组
            eligible_units = [(unit, efficiency_factors[unit.unit_id]) for unit in self.units if
                              unit.unit_id in [14, 15, 24, 25, 34, 35] and unit != self.last_unit]

        # 询问用户是否添加健康信息
        add_health_info = input("是否添加健康信息？(yes/no): ").lower() == "yes"

        # 针对每个机组询问健康评分并更新健康系数
        for unit in self.units:
            if add_health_info:
                health_coefficient = float(input(f"请输入 Unit {unit.unit_id} 的健康评分 (k >= 1): "))
                unit.health_coefficient = health_coefficient
            else:
                # TODO 可能？健康评分恢复初始值
                pass

        # 选择机组时考虑节能系数和健康系数
        # selected_unit, efficiency = min(eligible_units,
        #                                 key=lambda x: x[0].total_runtime / (x[1] * x[0].health_coefficient))

        minList = []
        minValue = 999999
        for x in eligible_units:
            cal = x[0].total_runtime + 336 * x[1] * x[0].health_coefficient
            if cal == minValue:
                minList.append(x)
            elif cal < minValue:
                minValue = cal
                minList = [x]

        if len(minList) == 1:
            selected_unit = minList[0]
        else:
            print("Select In")

        # 更新上次开机的机组
        self.last_unit = selected_unit

        # 返回选择的机组
        return selected_unit.unit_id


# 更新节能系数
# 定义节能系数和健康系数
efficiency_factors = {
    12: 0.9,
    13: 1.0,
    23: 1.2,
    14: 1.0,
    15: 1.5,
    24: 1.5,
    25: 1.0,
    34: 1.5,
    35: 1.0
}
health_factors = {
    12: 1.0,
    13: 1.0,
    23: 1.0,
    14: 1.0,
    15: 1.0,
    24: 1.0,
    25: 1.0,
    34: 1.0,
    35: 1.0
}

# 创建机组实例
units = [Unit(12), Unit(13), Unit(23), Unit(14), Unit(15), Unit(24), Unit(25), Unit(34), Unit(35)]

# 创建字典来跟踪每个子单元的总运行时间
sub_unit_runtimes = {}
sub_unit_record = {}

# 询问用户总次数
total_iterations = int(input("请输入总次数: "))

# 创建状态机实例
state_machine = PumpStationStateMachine(units)

for iteration in range(total_iterations):
    water_flow = int(input("请输入水量: "))

    # 选择下一个周期应该开启的机组
    selected_unit = state_machine.select_unit(water_flow)

    # 获取上次开机的机组并增加运行时间
    if state_machine.last_unit:
        for unit in units:
            if unit.unit_id == state_machine.last_unit.unit_id:
                unit.add_runtime(336)  # 假设每次测验开机时间为336小时

    # 输出结果，每个机组的累计运行时间，乘以节能系数
    for unit in units:
        efficiency = efficiency_factors.get(unit.unit_id, 1.0)
        total_runtime = unit.total_runtime
        print(f"Unit {unit.unit_id} total runtime: {total_runtime:.1f}h")
    print(f"In the two weeks, selected unit: {selected_unit}")

    # 输出每个子单元的累计运行时间
    for sub_unit, runtime in sub_unit_runtimes.items():
        print(f"Unit {sub_unit} total runtime: {runtime:.1f}h", sub_unit_record[sub_unit])


