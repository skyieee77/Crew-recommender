# -*- coding: utf-8 -*-
"""
@Project ：hww 
@File    ：unit.py
@Author  ：Knkiss
@Date    ：2023/9/25 19:38 
"""
import math
from decimal import Decimal as d
from random import random

efficiency_dict = {
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


class Unit:
    def __init__(self, name):
        self.name = name
        self.health_weight = 1.
        self.work_time = 0.
        self.work_time_total = 0.
        # 记录机组工作时间的字符串。
        self.record = ''

    # 工作时间保留小数 todo
    def __str__(self):
        return "机组:" + str(self.name) + \
            " 工作时间:" + str((self.work_time)) + \
            " 工作总时间:" + str(int(self.work_time_total))

    # add_work_time 方法用于向机组添加工作时间
    def add_work_time(self, time, efficient):
        a = d(str(time))
        b = d(str(self.health_weight))
        c = d(str(efficient))

        # d(str( ？？
        add_time = float(a * b * c)

        self.work_time += add_time
        self.work_time_total += add_time
        self.record += str(time) + '*' + str(self.health_weight) + '*' + str(efficient) + ' + '


class UnitManager:
    def __init__(self, LUN, SUN):
        self.large_unit_number = LUN
        self.small_unit_number = SUN
        self.large_unit = []
        self.small_unit = []

        # ？
        for i in range(self.large_unit_number):
            self.large_unit.append(Unit(i + 1))
        for i in range(self.small_unit_number):
            self.small_unit.append(Unit(self.large_unit_number + i + 1))

        self.work_large_unit = []
        self.work_small_unit = []
        self.change_list = [[], []]
        self.time_num = 0

    def nextTime(self, water_flow):
        self.time_num += 1
        # 将上一个时间周期的大机组和小机组加入到 last_work 列表中，
        last_work = []
        last_work.extend(self.work_large_unit)
        last_work.extend(self.work_small_unit)
        # 初始化一个变量 change，用于表示是否需要切换机组
        change = False
        # 定义流量阈值 todo 加了流量滞回，好像没什么用  9.27
        upper_threshold = 7150
        lower_threshold = 6900

        size = len(self.change_list[0]) + len(self.change_list[1])
        # 只有一大  运行机组就一个  处理水流量需求增加的情况，并触发机组切换的逻辑
        if size > 0 and water_flow > upper_threshold and len(self.work_large_unit) != 2:
            change = True
            print("水量需求增加，触发切机: ", end='')

            large_select = self.large_unit
            # 大的放入备选，因素是work time todo 根据大机组的工作总时间对 large_select 列表进行排序，将工作时间最短的排在前面。
            sorted_list = sorted(large_select, key=lambda x: x.work_time_total)
            # todo ?排序如何体现？？从已经切换的机组列表 self.change_list[0] 中，根据工作总时间进行排序，将工作时间最长的排在前面。
            # 要待机的机组 选择一个最大的待机
            remove_list = sorted(self.change_list[0], key=lambda x: x.work_time_total)

            # 如果有机组在待机列表中，移除工作时间最长的一个大机组，以确保不会选择待机的机组。
            if len(remove_list) > 0:
                sorted_list.remove(remove_list[-1])

            # todo  剩下的机组作为选择的机组，选择工作时间最短的两个大机组作为下一个时间周期的工作机组。
            next_work_unit = [sorted_list[0], sorted_list[1]]

            # ：将机组的工作时间重置为0
            for i in self.work_small_unit:
                i.work_time = 0.
            self.work_small_unit = []
            for i in self.work_large_unit:
                if i not in next_work_unit:
                    i.work_time = 0.
            self.work_large_unit = next_work_unit
        #     todo  小流量但没有45机组
        elif size > 0 and water_flow < lower_threshold and len(self.work_small_unit) != 1:
            change = True
            print("水量需求减少，触发切机: ", end='')

            large_select = self.large_unit
            sorted_list_large = sorted(large_select, key=lambda x: x.work_time_total)

            # 大机组可能切换
            remove_list = sorted(self.change_list[0], key=lambda x: x.work_time_total)
            for i in remove_list:
                sorted_list_large.remove(i)
            next_work_unit_large = [sorted_list_large[0]]

            # 选择小机组
            small_select = self.small_unit
            sorted_list_small = sorted(small_select, key=lambda x: x.work_time_total)
            next_work_unit_small = [sorted_list_small[0]]

            for i in self.work_large_unit:
                if i not in next_work_unit_large:
                    i.work_time = 0.
            self.work_large_unit = next_work_unit_large
            for i in self.work_small_unit:
                if i not in next_work_unit_small:
                    i.work_time = 0.
            self.work_small_unit = next_work_unit_small
        elif len(self.change_list[0]) != 0 or len(self.change_list[1]) != 0:
            change = True
            print("单次工作时长达到上限，触发切机: ", end='')

            if len(self.change_list[0]) != 0:
                sorted_list = sorted(self.large_unit, key=lambda x: x.work_time_total)
                remove_list = sorted(self.change_list[0], key=lambda x: x.work_time_total)
                sorted_list.remove(remove_list[-1])
                if len(self.work_large_unit) == 2:
                    next_work_unit_large = [sorted_list[0], sorted_list[1]]
                else:
                    next_work_unit_large = [sorted_list[0]]

                for i in self.work_large_unit:
                    if i not in next_work_unit_large:
                        i.work_time = 0.
                self.work_large_unit = next_work_unit_large
            if len(self.change_list[1]) != 0:
                sorted_list = sorted(self.small_unit, key=lambda x: x.work_time_total)
                remove_list = sorted(self.change_list[1], key=lambda x: x.work_time_total)
                sorted_list.remove(remove_list[-1])
                next_work_unit_small = [sorted_list[0]]

                for i in self.work_small_unit:
                    if i not in next_work_unit_small:
                        i.work_time = 0.
                self.work_small_unit = next_work_unit_small

        if change:
            now_work = []
            now_work.extend(self.work_large_unit)
            now_work.extend(self.work_small_unit)

            for i in last_work:
                print(i.name, end=',')
            print(" -> ", end='')
            for i in now_work:
                print(i.name, end=',')
            print("\n当前工作轮次:" + str(self.time_num) + "\n当前工作状态: ")
            self.report()
            print("-------------------------------------")

        self.add_work_time()  # 计算当前周期结果并储存
        self.change_list = self.check_work_time()

    # get_efficiency法根据当前工作机组的组合计算效率。
    def get_efficiency(self):
        work_unit = []
        work_unit.extend(self.work_large_unit)
        work_unit.extend(self.work_small_unit)
        work_unit = sorted(work_unit, key=lambda x: x.name)
        group = 0
        for i in work_unit:
            group *= 10
            group += i.name
        res = efficiency_dict[group]
        return res

    def add_work_time(self, debug=1):
        efficiency_data = self.get_efficiency()
        for i in self.work_large_unit:
            assert isinstance(i, Unit)
            i.add_work_time(debug, efficiency_data)
        for i in self.work_small_unit:
            assert isinstance(i, Unit)
            i.add_work_time(debug, efficiency_data)

    # check_work_time方法检查工作时间是否超过了最大工作时间，如果超过了则返回需要切换的机组。
    def check_work_time(self, max_work_time=336):
        large_change_unit = []
        for i in self.work_large_unit:
            assert isinstance(i, Unit)
            if i.work_time > max_work_time:
                large_change_unit.append(i)
        small_change_unit = []
        for i in self.work_small_unit:
            assert isinstance(i, Unit)
            if i.work_time > max_work_time:
                small_change_unit.append(i)
        return large_change_unit, small_change_unit

    def report(self):
        for i in self.large_unit:
            print(i)
        for i in self.small_unit:
            print(i)

    def init_work(self, unit_list):
        for i in unit_list:
            for j in self.small_unit:
                if i == j.name:
                    self.work_small_unit.append(j)
            for j in self.large_unit:
                if i == j.name:
                    self.work_large_unit.append(j)


if __name__ == '__main__':
    large_unit_number = 3
    small_unit_number = 2
    um = UnitManager(large_unit_number, small_unit_number)

    um.init_work([1,2])
    # 打开文本文件并读取 "出站流量" 列数据
    with open('E:\Code\pythonProject4\data\merged_data4.txt', 'r', encoding='UTF8') as file:

        lines = file.readlines()
        # 逐行读取数据并传递给 um.nextTime 方法
        for line in lines[1:]:
            # 解析第10列数据（假设第10列是索引为9的列）
            data_columns = line.replace('\n', '').split('\t')
            flow_data = float(data_columns[9])
            um.nextTime(flow_data)

print('finish')

