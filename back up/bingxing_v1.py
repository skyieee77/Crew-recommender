from matplotlib import pyplot as plt

import sys
import numpy as np
import datetime
import pymysql
import json


if __name__ == '__main__':  ### 1 json数据传过来

    # 1.1 把json数据转换成字典
    data = json.loads(sys.argv)

    ### 2 从MySQL数据库提取历史水位数据和水量数据

    # 连接数据库
    con = pymysql.connect(host='10.207.6.14', password='znbz@2022', port=3306, user='znbz', charset='utf8mb4',
                          database='vici_zhinengbengzhan')
    # 创建游标对象
    cur = con.cursor()

    # 执行SQL查询
    # 最新60分钟的水位数据，升序
    # select 玉泉山水位,杏石口水位,麻峪水位 from (水位表 order by 时间 desc limit 60) as 最新数据 order by 时间 asc
    query1 = "select yqs_inlt,xsk_inlt,my_inlt from (znbz_python_data1 order by create_time desc limit 60) as latest_data_inlt order by create_time asc"
    cur.execute(query1)
    result1 = cur.fetchall()
    # 取最新的水位
    H_yu = [row[0] for row in result1[-1]]
    H_xing = [row[1] for row in result1[-1]]
    H_mayu = [row[2] for row in result1[-1]]

    # 最新180分的瞬时流量数据，升序
    # select 麻峪瞬时水量,杏石口瞬时水量,玉泉山瞬时水量,杏石口入水口（分水口）瞬时水量,石景山南线瞬时水量,石景山北线瞬时水量,退水口瞬时水量 from (流量表 order by 时间 desc limit 180) as 最新数据 order by 时间 asc
    query2 = "select my_hft,xsk_hft,yqs_hft,in_hft,south_hft,north_hft,re_hft from (znbz_python_data2 order by create_time desc limit 180) as latest_data_hft order by create_time asc"
    cur.execute(query2)
    result2 = cur.fetchall()
    # 提取麻峪、杏石口瞬时水量最新6分钟的数据，并计算均值
    selected_data_mayu = [row[0] for row in result2[-6:]]
    selected_data_xing = [row[1] for row in result2[-6:]]
    selected_data_nan = [row[4] for row in result2[-6:]]
    selected_data_bei = [row[5] for row in result2[-6:]]
    selected_data_tui = [row[6] for row in result2[-6:]]
    mean_value_mayu = sum(selected_data_mayu) / len(selected_data_mayu)
    mean_value_xing = sum(selected_data_xing) / len(selected_data_xing)
    mean_value_shi = sum(selected_data_nan) / len(selected_data_nan) + sum(selected_data_bei) / len(selected_data_bei)
    mean_value_tui = sum(selected_data_tui) / len(selected_data_tui)

    # 最新180分的累计流量数据，升序
    # select 麻峪累计水量,杏石口累计水量,玉泉山累计水量,杏石口入水口（分水口）累计水量,石景山南线累计水量,石景山北线累计水量,退水口累计水量 from (流量表 order by 时间 desc limit 180) as 最新数据 order by 时间 asc
    query3 = "select my_tft,xsk_tft,yqs_tft,in_tft,south_tft,north_tft,re_tft from (znbz_python_data2 order by create_time desc limit 180) as latest_data_tft order by create_time asc"
    cur.execute(query3)
    result3 = cur.fetchall()

    # 3 算法部分

    城子水厂流量 = data['cz']
    麻峪流量 = mean_value_mayu
    石景山水厂输水量 = mean_value_shi
    永引渠退水量 = mean_value_tui

    # 麻峪初始、目标水位
    麻峪初始水位 = H_mayu
    麻峪目标水位 = data['13_inlt']

    # 杏石口初始、目标水位
    杏石口初始水位 = H_xing
    杏石口目标水位 = data['12_inlt']

    # 前池横截面积
    杏石口横截面积 = 1800
    麻峪横截面积 = 750

    # 频率
    玉泉山频率上限 = data['11_max_f']
    玉泉山频率下限 = data['11_min_f']
    杏石口频率上限 = data['12_max_f']
    杏石口频率下限 = data['12_min_f']
    麻峪频率上限 = data['13_max_f']
    麻峪频率下限 = data['13_min_f']

    # 流量-频率特性
    玉泉山流量上限 = 362.08 * 玉泉山频率上限 - 6473.72
    玉泉山流量下限 = 362.08 * 玉泉山频率下限 - 6473.72
    杏石口流量上限 = 179.02 * 杏石口频率上限 - 4909.6
    杏石口流量下限 = 179.02 * 杏石口频率下限 - 4909.6
    麻峪流量上限 = 130.8 * 麻峪频率上限 - 2129.69
    麻峪流量下限 = 130.8 * 麻峪频率下限 - 2129.69

    # 换算
    玉泉山流量上限 = 玉泉山流量上限 / 3600
    玉泉山流量下限 = 玉泉山流量下限 / 3600
    杏石口流量上限 = 杏石口流量上限 / 3600
    杏石口流量下限 = 杏石口流量下限 / 3600
    麻峪流量上限 = 麻峪流量上限 / 3600
    麻峪流量下限 = 麻峪流量下限 / 3600

    城子水厂流量 = 城子水厂流量 / 3600
    麻峪流量 = 麻峪流量 / 3600
    石景山水厂输水量 = 石景山水厂输水量 / 3600
    永引渠退水量 = 永引渠退水量 / 3600

    # 流量转换为频率
    def F_yu(Q):
        f_yu = (Q + 6473.72) / 362.08
        return round(f_yu, 2)

    def F_xing(Q):
        f_xing = (Q + 4909.6) / 179.02
        return round(f_xing, 2)

    def F_mayu(Q):
        f_mayu = (Q + 2129.69) / 130.8
        return round(f_mayu, 2)

    # 1是上升，0是下降，2是不动
    def status(杏石口目标水位, 杏石口初始水位, 麻峪目标水位, 麻峪初始水位):
        D1 = 杏石口目标水位 - 杏石口初始水位
        D2 = 麻峪目标水位 - 麻峪初始水位

        if D1 > 0:
            status1 = 1
        elif D1 == 0:
            status1 = 2
        else:
            status1 = 0

        if D2 > 0:
            status2 = 1
        elif D2 == 0:
            status2 = 2
        else:
            status2 = 0

        return status1, status2

    ### 调度规则
    # 若上升，选流量上限；若下降，选流量下限
    def Q_saturation(status1, status2):

        if status2 == 1:
            Q2 = 杏石口流量上限
        elif status2 == 2:
            Q2 = 麻峪流量
        else:
            Q2 = 杏石口流量下限

        if status1 == 1:
            Q1 = 玉泉山流量上限
        elif status1 == 2:
            Q1 = Q2 + (石景山水厂输水量 + 永引渠退水量)
        else:
            # 细节：玉泉山的流量选取下限时，不能小于 (石景山水厂输水量 + 永引渠退水量)
            if (石景山水厂输水量 + 永引渠退水量) > 玉泉山流量下限:
                Q1 = 石景山水厂输水量 + 永引渠退水量
            else:
                Q1 = 玉泉山流量下限

        return round(Q1, 2), round(Q2, 2)

    # 计算速度
    def V1_xing(Q1, Q2, Q4, Q5, sq1):
        v1 = (Q1 - Q2 - Q4 - Q5) / sq1
        return v1

    def V2_mayu(Q2, Q3, sq2):
        v2 = (Q2 - Q3) / sq2
        return v2

    # 控制输出 u = Q
    def control_u1(r1, s1, u2, Q4, Q5):
        u1 = r1 * s1 + u2 + Q4 + Q5

        if u1 > 玉泉山流量上限:
            u1 = 玉泉山流量上限
        elif u1 < (石景山水厂输水量 + 永引渠退水量):
            u1 = (石景山水厂输水量 + 永引渠退水量)

        return round(u1, 2)

    def control_u2(r2, s2, Q3):
        u2 = r2 * s2 + Q3

        if u2 > 杏石口流量上限:
            u2 = 杏石口流量上限
        elif u2 < 杏石口流量下限:
            u2 = 杏石口流量下限

        return round(u2, 2)

    # 通过调度规则，给定期望调节速率 m/s
    status1, status2 = status(杏石口目标水位, 杏石口初始水位, 麻峪目标水位, 麻峪初始水位)
    Q1, Q2 = Q_saturation(status1, status2)
    V1 = V1_xing(Q1, Q2, 石景山水厂输水量, 永引渠退水量, 杏石口横截面积)  # 杏石口期望调节速率
    V2 = V2_mayu(Q2, 麻峪流量, 麻峪横截面积)  # 麻峪期望调节速率

    # 输入信号 速率
    输入信号1 = V1
    输入信号2 = V2

    # 控制输出 u = Q
    u2 = control_u2(输入信号2, 麻峪横截面积, 麻峪流量)
    u1 = control_u1(输入信号1, 杏石口横截面积, Q2, 石景山水厂输水量, 永引渠退水量)

    Q1_c = u1
    Q2_c = u2
    麻峪流量 = 城子水厂流量

    # 实际调节速率 V
    V11 = V1_xing(Q1_c, Q2_c, 石景山水厂输水量, 永引渠退水量, 杏石口横截面积)
    V22 = V2_mayu(Q2_c, 麻峪流量, 麻峪横截面积)

    # 输出信号 当前水位
    H11 = []  # 存储所有时刻的当前水位
    H22 = []  # 存储所有时刻的当前水位
    H11.append(杏石口初始水位)
    H22.append(麻峪初始水位)

    Q11 = []  # 存储所有时刻的输出流量
    Q22 = []  # 存储所有时刻的输出流量
    Q33 = []
    Q11.append(Q1_c)
    Q22.append(Q2_c)
    Q33.append(麻峪流量)

    H1 = 杏石口初始水位  # 当前水位
    H2 = 麻峪初始水位  # 当前水位

    # 开始的时候
    # 当前时间
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y年%m月%d日 %H:%M")
    print("当前时间：", formatted_time)

    f_yu = F_yu(Q1_c * 3600)
    f_xing = F_xing(Q2_c * 3600)
    f_mayu = F_mayu(麻峪流量 * 3600)

    # 存储调节的时间、哪个站调、流量调为多少、机组频率为多少
    data_var = []

    data_var.append(formatted_time)
    data_var.append(11)
    data_var.append(round(Q1_c * 3600, 2))
    data_var.append(data['11_machine_now'])
    data_var.append(f_yu)
    data_var.append(12)
    data_var.append(round(Q2_c * 3600, 2))
    data_var.append(data['11_machine_now'])
    data_var.append(f_xing)
    data_var.append(13)
    data_var.append(round(麻峪流量 * 3600, 2))
    data_var.append(data['13_machine_now'])
    data_var.append(f_mayu)

    print("{}时，麻峪流量调节为{}m³，杏石口流量调节为{}m³，玉泉山流量调节为{}m³".format(formatted_time, 麻峪流量 * 3600, Q2_c * 3600, Q1_c * 3600))

    ### 总思路
    # 1 看哪个前池先到目标水位
    # 2.1 若麻峪先到，V2 = 0，通过控制器更新Q2和Q1；后杏石口到，V1 = 0，通过控制器更新Q1
    # 2.2 若杏石口先到，V1 = 0，通过控制器更新Q1；后麻峪到，V1 = 0，通过控制器更新Q2和Q1
    # 注意：更新Q2时，必须更新Q1，因为根据公式，Q2的变化会引起Q1的变化

    # 调节时间1小时
    T = 3600

    for i in range(1, T):
        H1 = V11 * i + 杏石口初始水位  # 更新当前水位
        H2 = V22 * i + 麻峪初始水位  # 更新当前水位
        H11.append(H1)
        H22.append(H2)
        Q11.append(Q1_c)
        Q22.append(Q2_c)
        Q33.append(麻峪流量)

        # 杏石口先到目标
        if abs(杏石口初始水位 - 杏石口目标水位) * 0.01 > abs(H1 - 杏石口目标水位):
            # 那么杏石口的速度要变成 0
            V11 = 0
            # 更新玉泉山输出流量  u1的变化不引起u2的变化，所以只更新u1
            Q1_c = control_u1(V11, 杏石口横截面积, Q2_c, 石景山水厂输水量, 永引渠退水量)
            # print("玉泉山长度：", len(Q11))
            # print("玉泉山的流量更新为：", Q1_c*3600)

            new_time_yu = current_time + datetime.timedelta(seconds=len(Q11))
            formatted_new_time_yu = new_time_yu.strftime("%Y年%m月%d日 %H:%M")

            f_yu = F_yu(round(Q1_c * 3600, 2))

            data_var.append(formatted_new_time_yu)
            data_var.append(11)
            data_var.append(round(Q1_c * 3600, 2))
            data_var.append(data['11_machine_now'])
            data_var.append(f_yu)

            print("{}时，玉泉山流量调节为{}m³".format(formatted_new_time_yu, round(Q1_c * 3600, 2)))
            break

        # 麻峪先到目标
        if abs(麻峪初始水位 - 麻峪目标水位) * 0.01 > abs(H2 - 麻峪目标水位):
            # 那么麻峪的速度要变成 0
            V22 = 0
            # 更新杏石口、玉泉山的输出流量  u2的变化引起u1的变化，所以更新u1和u2
            Q2_c = control_u2(V22, 麻峪横截面积, 麻峪流量)
            # Q1_c = control_u1(V11, 杏石口横截面积, Q2_c, 石景山水厂输水量, 永引渠退水量)

            Q1, Q2 = Q_saturation(status1, status2)
            V11 = V1_xing(Q1, Q2_c, 石景山水厂输水量, 永引渠退水量, 杏石口横截面积)
            Q1_c = control_u1(V11, 杏石口横截面积, Q2_c, 石景山水厂输水量, 永引渠退水量)

            # u1和u2都更新了，所以要更新V11
            V11 = V1_xing(Q1_c, Q2_c, 石景山水厂输水量, 永引渠退水量, 杏石口横截面积)
            # print("玉泉山长度：", len(Q11))
            # print("杏石口长度：", len(Q22))
            # print("玉泉山的流量更新为：", Q1_c*3600)
            # print("杏石口的流量更新为：", Q2_c*3600)

            new_time_yu = current_time + datetime.timedelta(seconds=len(Q11))
            new_time_xing = current_time + datetime.timedelta(seconds=len(Q22))
            formatted_new_time_yu = new_time_yu.strftime("%Y年%m月%d日 %H:%M")
            formatted_new_time_xing = new_time_xing.strftime("%Y年%m月%d日 %H:%M")

            f_yu = F_yu(Q1_c * 3600)
            f_xing = F_xing(Q2_c * 3600)

            data_var.append(formatted_new_time_yu)
            data_var.append(11)
            data_var.append(round(Q1_c * 3600, 2))
            data_var.append(data['11_machine_now'])
            data_var.append(f_yu)
            data_var.append(12)
            data_var.append(round(Q2_c * 3600, 2))
            data_var.append(data['12_machine_now'])
            data_var.append(f_xing)

            print("{}时，杏石口流量调节为{}m³，玉泉山流量调节为{}m³".format(formatted_new_time_yu, Q2_c * 3600, Q1_c * 3600))
            break

        # 麻峪不动，杏石口到了目标
        if (abs(杏石口初始水位 - 杏石口目标水位) * 0.01 > abs(H1 - 杏石口目标水位)) & (status2 == 2):
            # 那么杏石口的速度要变成 0
            V11 = 0
            # 更新玉泉山输出流量

            Q1_c = control_u1(V11, 杏石口横截面积, Q2_c, 石景山水厂输水量, 永引渠退水量)
            # print("玉泉山长度：", len(Q11))
            # print("玉泉山的流量更新为：", Q1_c*3600)

            new_time_yu = current_time + datetime.timedelta(seconds=len(Q11))
            formatted_new_time_yu = new_time_yu.strftime("%Y年%m月%d日 %H:%M")

            f_yu = F_yu(Q1_c * 3600)

            data_var.append(formatted_new_time_yu)
            data_var.append(11)
            data_var.append(round(Q1_c * 3600, 2))
            data_var.append(data['11_machine_now'])
            data_var.append(f_yu)

            print("{}时，玉泉山流量调节为{}m³".format(formatted_new_time_yu, Q1_c * 3600))
            break

    temp_H = H1
    temp = 1
    if (status1 != 2) & (status2 != 2):
        for j in range(i + 1, T):
            # 杏石口先到目标
            if abs(杏石口初始水位 - 杏石口目标水位) * 0.01 > abs(H1 - 杏石口目标水位):
                # 麻峪继续更新当前水位
                H2 = V22 * j + 麻峪初始水位
                H11.append(H1)
                H22.append(H2)
                Q11.append(Q1_c)
                Q22.append(Q2_c)
                Q33.append(麻峪流量)
                # 麻峪后到目标
                if abs(麻峪初始水位 - 麻峪目标水位) * 0.01 > abs(H2 - 麻峪目标水位):
                    # 那么麻峪的速度要变成 0
                    V22 = 0
                    # 更新杏石口、玉泉山的输出流量  u2的变化引起u1的变化，所以更新u1和u2
                    Q2_c = control_u2(V22, 麻峪横截面积, 麻峪流量)

                    Q1_c = control_u1(V11, 杏石口横截面积, Q2_c, 石景山水厂输水量, 永引渠退水量)
                    # print("杏石口长度：", len(Q22))
                    # print("玉泉山的流量更新为：", Q1_c*3600)
                    # print("杏石口的流量更新为：", Q2_c*3600)

                    new_time_yu = current_time + datetime.timedelta(seconds=len(Q11))
                    new_time_xing = current_time + datetime.timedelta(seconds=len(Q22))
                    formatted_new_time_yu = new_time_yu.strftime("%Y年%m月%d日 %H:%M")
                    formatted_new_time_xing = new_time_xing.strftime("%Y年%m月%d日 %H:%M")

                    f_yu = F_yu(Q1_c * 3600)
                    f_xing = F_xing(Q2_c * 3600)

                    data_var.append(formatted_new_time_yu)
                    data_var.append(11)
                    data_var.append(round(Q1_c * 3600, 2))
                    data_var.append(data['11_machine_now'])
                    data_var.append(f_yu)
                    data_var.append(12)
                    data_var.append(round(Q2_c * 3600, 2))
                    data_var.append(data['12_machine_now'])
                    data_var.append(f_xing)

                    print("{}时，杏石口流量调节为{}m³，玉泉山流量调节为{}m³".format(formatted_new_time_yu, Q2_c * 3600, Q1_c * 3600))
                    break

            # 麻峪先到目标
            if abs(麻峪初始水位 - 麻峪目标水位) * 0.01 > abs(H2 - 麻峪目标水位):
                # 杏石口继续更新当前水位
                H1 = V11 * temp + temp_H
                H11.append(H1)
                H22.append(H2)
                Q11.append(Q1_c)
                Q22.append(Q2_c)
                Q33.append(麻峪流量)
                temp = temp + 1
                # 杏石口后到目标
                if abs(杏石口初始水位 - 杏石口目标水位) * 0.01 > abs(H1 - 杏石口目标水位):
                    # 那么杏石口的速度要变成 0
                    V11 = 0
                    # 更新玉泉山输出流量
                    Q1_c = control_u1(V11, 杏石口横截面积, Q2_c, 石景山水厂输水量, 永引渠退水量)
                    # print("玉泉山长度：", len(Q11))
                    # print("玉泉山的流量更新为：", Q1_c*3600)

                    new_time_yu = current_time + datetime.timedelta(seconds=len(Q11))
                    formatted_new_time_yu = new_time_yu.strftime("%Y年%m月%d日 %H:%M")

                    f_yu = F_yu(Q1_c * 3600)

                    data_var.append(formatted_new_time_yu)
                    data_var.append(11)
                    data_var.append(round(Q1_c * 3600, 2))
                    data_var.append(data['11_machine_now'])
                    data_var.append(f_yu)

                    print("{}时，玉泉山流量调节为{}m³".format(formatted_new_time_yu, Q1_c * 3600))
                    break

    if (status1 != 2) & (status2 != 2):
        for z in range(j + 1, T):
            H11.append(H1)
            H22.append(H2)
            Q11.append(Q1_c)
            Q22.append(Q2_c)
            Q33.append(麻峪流量)
    else:
        # 麻峪不动，杏石口到了目标
        for z in range(i + 1, T):
            if (abs(杏石口初始水位 - 杏石口目标水位) * 0.01 > abs(H1 - 杏石口目标水位)) & (status2 == 2):
                H11.append(H1)
                H22.append(H2)
                Q11.append(Q1_c)
                Q22.append(Q2_c)
                Q33.append(麻峪流量)

        # 杏石口不动，麻峪到了目标
        for z in range(i + 1, T):
            if (abs(麻峪初始水位 - 麻峪目标水位) * 0.01 > abs(H2 - 麻峪目标水位)) & (status1 == 2):
                H11.append(H1)
                H22.append(H2)
                Q11.append(Q1_c)
                Q22.append(Q2_c)
                Q33.append(麻峪流量)

    Q11 = [x * 3600 for x in Q11]
    Q22 = [y * 3600 for y in Q22]
    Q33 = [z * 3600 for z in Q33]

    # 每分钟的水位
    H111 = []
    H222 = []
    for index, value in enumerate(H11):
        if index % 60 == 0:
            value = round(value, 2)
            H111.append(value)
    for index, value in enumerate(H22):
        if index % 60 == 0:
            value = round(value, 2)
            H222.append(value)

    # 4 输出转成json
    data_var = json.dumps(data_var)  # 什么时候，哪个站，流量调节为多少，哪台机组，频率调节为多少
    H111 = json.dumps(H111)  # 1小时，每分钟的杏石口水位
    H222 = json.dumps(H222)  # 1小时，每分钟的麻峪水位

    print(data_var, H111, H222)
    #return data_var, H111, H222  # 5 返回