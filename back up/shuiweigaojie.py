# # -*- coding: UTF-8 -*-
"""
@Project ：hww
@File    ：unit.py
@Author  ：Knkiss
@Date    ：2023/10/16 19:38
"""
# todo 方案 1 仅规划步长，写入excel
import pandas as pd
import openpyxl
from openpyxl.styles import Font


target_level1 = float(94.8)
current_level1 = float(input("请输入麻峪当前水位（按Enter键结束输入）: "))


target_level2 =float(64.5)
current_level2 = float(input("请输入杏石口当前水位（按Enter键结束输入）: "))

def calculate_adjustment(target_level1, current_level1, normal_descent=0.03):

    steps = 0
    adjusted_level = current_level1

    data1 = []  # 用于存储水位数据

    while abs(adjusted_level - target_level1) > 0.001:  # 限定小于0.001以允许小于0.03的调整
        if target_level1 > adjusted_level:
            step_adjustment = min(normal_descent, target_level1 - adjusted_level)
        else:
            step_adjustment = max(-normal_descent, target_level1 - adjusted_level)

        adjusted_level += step_adjustment
        steps += 1
        data1.append(adjusted_level)

    return data1








def calculate_adjustment2(target_level2, current_level2, normal_descent=0.03):
    steps = 0
    adjusted_level = current_level2

    data = []  # 用于存储水位数据

    while abs(adjusted_level - target_level2) > 0.001:  # 限定小于0.001以允许小于0.03的调整
        if target_level2 > adjusted_level:
            step_adjustment = min(normal_descent, target_level2 - adjusted_level)
        else:
            step_adjustment = max(-normal_descent, target_level2 - adjusted_level)

        adjusted_level += step_adjustment
        steps += 1
        data.append(adjusted_level)

    return data



water_levels = calculate_adjustment(target_level1, current_level1)

# 创建一个空的DataFrame
df = pd.DataFrame()

# 插入水位数据和空行
for i, level in enumerate(water_levels):
    df = pd.concat([df, pd.DataFrame({'水位 (m)': [level]})], ignore_index=True)
    if i < len(water_levels) - 1:
        for _ in range(5):
            df = pd.concat([df, pd.DataFrame({'水位 (m)': [None]})], ignore_index=True)

# 创建一个Excel writer对象
with pd.ExcelWriter('../data/调试2023.xlsx', engine='xlsxwriter') as writer:
    # todo 修改插入起始行、列
    df.to_excel(writer, sheet_name='水位数据', startrow=12, startcol=8, index=False, header=False)
    workbook = writer.book
    worksheet = writer.sheets['水位数据']

print("水位数据已成功写入Excel文件。")



water_levels2 = calculate_adjustment2(target_level2, current_level2)

# 创建一个空的DataFrame
df1 = pd.DataFrame()

# 插入水位数据和空行
for i, level in enumerate(water_levels2):
    df1 = pd.concat([df1, pd.DataFrame({'水位 (m)': [level]})], ignore_index=True)
    if i < len(water_levels2) - 1:
        for _ in range(5):
            df1 = pd.concat([df1, pd.DataFrame({'水位 (m)': [None]})], ignore_index=True)

# 创建一个Excel writer对象
with pd.ExcelWriter('../data/调试2023.xlsx', engine='xlsxwriter') as writer:
    # todo 修改插入起始行、列
    df1.to_excel(writer, sheet_name='水位数据', startrow=12, startcol=9, index=False, header=False)
    workbook = writer.book
    worksheet = writer.sheets['水位数据']

print("水位数据已成功写入Excel文件。")




calculate_adjustment(target_level1, current_level1)
calculate_adjustment2(target_level2, current_level2)

# todo 写入excel
# water_levels = calculate_adjustment2(target_level2, current_level2)
#
# # 插入空5行
# for i in range(1, len(water_levels), 6):
#     water_levels[i:i] = [None] * 5
#
# # 创建一个Excel DataFrame
# df = pd.DataFrame(water_levels, columns=['水位 (m)'])
#
# # 创建一个Excel writer对象
# with pd.ExcelWriter('水位数据.xlsx', engine='xlsxwriter') as writer:
#     df.to_excel(writer, sheet_name='水位数据', startrow=0, startcol=1, index=False, header=False)
#     workbook = writer.book
#     worksheet = writer.sheets['水位数据']
#
# print("水位数据已成功写入Excel文件。")



# # 创建一个Excel DataFrame
# df = pd.DataFrame(water_levels, columns=['水位 (m)'])
#
# # 添加空5行
# empty_rows = [None] * 5
# for _ in range(1, len(water_levels), 6):
#     water_levels[_:_] = empty_rows
#
# # 创建一个Excel writer对象
# with pd.ExcelWriter('水位数据.xlsx', engine='xlsxwriter') as writer:
#     df.to_excel(writer, sheet_name='水位数据', startrow=0, startcol=1, index=False, header=False)
#     workbook = writer.book
#     worksheet = writer.sheets['水位数据']
#
# print("水位数据已成功写入Excel文件。")

#todo 方案2 规划加校正

# class ShuiWei:
#     def __init__(self, current, target):
#         self.current = current
#         self.target = target
#         self.origin_project = [self.current]
#         self.refresh_project = None
#         if current > target:
#             self.type = 0  # 1=上升 0=下降
#         else:
#             self.type = 1  # 1=上升 0=下降
#         self.init_project()
#
#     def init_project(self):
#         current = self.current
#         if self.type == 1:
#             while current < self.target:
#                 current = (int(round(current * 100)) + 3) / 100
#                 if current > self.target:
#                     self.origin_project.append(self.target)
#                 else:
#                     self.origin_project.append(current)
#         else:
#             while current > self.target:
#                 current = (int(round(current * 100)) - 3) / 100
#                 if current < self.target:
#                     self.origin_project.append(self.target)
#                 else:
#                     self.origin_project.append(current)
#         self.refresh_project = self.origin_project.copy()
#
#     def print(self):
#         print("\n计划运行图")
#         step = 0
#         for i in range(len(self.refresh_project)):
#             project = self.origin_project[i]
#             changed = self.refresh_project[i]
#             add_str = ", 按计划运行"
#
#             if project != changed:
#                 if self.type == 1:
#                     modify = changed - project
#                 else:
#                     modify = project - changed
#                 next_modify = 0.03 - modify
#                 if next_modify + changed > self.target and self.type == 1:
#                     next_modify = self.target - changed
#                 elif changed - next_modify < self.target and self.type == 0:
#                     next_modify = changed - self.target
#
#                 add_str = " [原计划{project:.2f}m], 下次调整{modify:.2f}m".format(project=project, modify=next_modify)
#
#             print("步长 {step:d}, 时间 {time:d} 分钟: 当前水位{changed:.2f}m"
#                   .format(step=step, changed=changed, time=step * 6) + add_str)
#             step += 1
#
#     def change_project(self, step, sensor):
#         self.refresh_project[step] = sensor
#
#
# if __name__ == '__main__':
#     shuiwei = ShuiWei(0.5, 0.6)
#     shuiwei.change_project(3, 0.51)
#     shuiwei.change_project(4, 0.55)
#     shuiwei.print()
#
#     shuiwei = ShuiWei(0.6, 0.5)
#     shuiwei.change_project(1, 0.56)
#     shuiwei.change_project(2, 0.53)
#     shuiwei.print()



#

# adjusted_level是理想水位

# # todo 不会？
# def error_correction(current_target, sensor_level, adjustment, step_time=6, normal_descent=0.03):
#
#
#     steps, adjusted_level = calculate_adjustment(target_level, current_level, normal_descent=0.03)
#
#     sensor_level=float(input("请输入传感器水位（按Enter键结束输入）: "))
#
#     adjustment=adjusted_level-sensor_level
#     next_time = 6 * steps
#     next_ajt = adjustment + normal_descent
#
#     # next_target
#
#     # todo
#     print(f"下一时刻需要修正：{next_ajt:.2f}m，在 {next_time} 分钟后")
#
#
#
#
#
#
#
#
#
# #
# # 示例测试
# error_correction('current_target', 'sensor_level','adjustment')
