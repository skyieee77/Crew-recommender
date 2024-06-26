# -*- coding: UTF-8 -*-
# ... 其他代码
# 定义机组类


# 不是的，输出的是单个单元运行时间，要单个单元运行时间不差太多，但每次决定启动都得2个单元在一起的，启动的必须是组合[Unit 12), Unit(13), Unit (23)、单元(14)、单元(15)、单元(24)、单元(25)、单元(34)、单元(35)]



# 很好，只是“每个模块的累计运行时间”指的是1号运行时间，2号运行时间，而不是12.可以再多个功能，输入开机总决定次数，在所有次数用完时尽可能让123大机组运行时间相等，45小机组运行时间相等
class Unit:
    def __init__(self, unit_id):
        self.unit_id = unit_id
        self.total_runtime = 0

    def add_runtime(self, hours):
        self.total_runtime += hours

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
        if water_flow > 7000:
            # 使用大机组
            large_units = [unit for unit in self.units if unit.unit_id in [12, 13, 23] and unit != self.last_unit]
            selected_unit = min(large_units, key=lambda x: x.total_runtime)
        else:
            # 使用小机组
            small_units = [unit for unit in self.units if unit.unit_id in [14, 15, 24, 25, 34, 35] and unit != self.last_unit]
            selected_unit = min(small_units, key=lambda x: x.total_runtime)

        # 更新上次开机的机组
        self.last_unit = selected_unit

        # 返回选择的机组
        return selected_unit.unit_id

# 创建机组实例
units = [Unit(12), Unit(13), Unit(23), Unit(14), Unit(15), Unit(24), Unit(25), Unit(34), Unit(35)]

# 创建状态机实例
state_machine = PumpStationStateMachine(units)

# 模拟输入10次测验
for i in range(10):
    water_flow = int(input("请输入水量: "))
    last_unit = int(input("请输入上次开机的机组: "))

    # 获取上次开机的机组并增加运行时间
    for unit in units:
        if unit.unit_id == last_unit:
            unit.add_runtime(2)  # 假设每次测验开机时间为2周

    # 选择下一个周期应该开启的机组
    selected_unit = state_machine.select_unit(water_flow)

    # 输出结果
    print(f"Next two weeks, selected unit: {selected_unit}")

    # 输出每个机组的累计运行时间
    for unit in units:
        print(f"Unit {unit.unit_id} total runtime: {unit.total_runtime} weeks")
