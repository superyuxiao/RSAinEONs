"""
Version: 1.8
Author: 于潇
Date:2020-05-2

04-11
网络初始化结构
Node节点类
Link链路类
Traffic业务类
04-12
修改Link类 两端节点   Traffic类 源节点目的节点
节点和链路都是链表格式输入消息
MST算法
04-13
selectlink 根据给定节点选定链路
部分节点MST算法，但是发现问题！“若有不相邻的节点，则算法不能正常运行” 考虑用最短路径算法将不相邻的节点连起来
构造NSFNET和USbackbone
04-15
编写最短路径算法（未完成）
04-16
完成最短路径算法 任意单节点到其他所有节点的最短路径
04-19
基于最短路径算法构建MPH（启发式最小成本算法） 观察后发现MPH等价与SPT+MST
04-20
完成MPH算法 FF算法
Traffic类在FF中调整参数，增加业务状态
04-21
SW计算
仿真环境：泊松到达时间
04-22
仿真环境，完成MPH-FF仿真测试
04-23
完成MPH-FF百万次仿真测试，得到实验数据
散着写比搞成一个函数要运行的快
04-27
完成MPSW  成了成了
05-02
完成了SWP-MPH
"""

from netclass import Node, Link, Traffic
from Algorithm import MST, SPT, MPH
import numpy as np
import random
import operator
import datetime
import matplotlib.pyplot as plt


def FF(tra):
    route = tra.alink
    slot_index = 0
    if len(route) != 0:
        for slot_index in range(0, 20 - tra.traslot):   # ##############################  这个20是每个链路的频隙数，不一定是一个固定值，注意！！！
            for link_index in range(0, len(route)):
                if route[link_index].linkslot[slot_index:slot_index + tra.traslot] != [1] * tra.traslot:
                    break
            if link_index == len(route) - 1:
                break
        if slot_index != 19 - tra.traslot:
            for link_index in range(0, len(route)):
                route[link_index].linkslot[slot_index:slot_index + tra.traslot] = [0] * tra.traslot
            tra.aslot.clear()
            tra.aslot.append(slot_index)
            for i in range(1, tra.traslot):
                tra.aslot.append(tra.aslot[0] + i)
            tra.status = 'Successful'
        else:
            tra.status = 'Failed'
    else:
        tra.status = 'Waiting'

    return slot_index


def First_Fit(route, traslot, sumslot):
    slot_index = 0
    if len(route) != 0:
        for slot_index in range(0, sumslot - traslot):
            for link_index in range(0, len(route)):
                if route[link_index].linkslot[slot_index:slot_index + traslot] != [1] * traslot:
                    break
            if link_index == len(route) - 1:
                break
        if slot_index != sumslot - 1 - traslot:
            for link_index in range(0, len(route)):
                route[link_index].linkslot[slot_index:slot_index + traslot] = [0] * traslot
            status = 'Successful'
        else:
            status = 'Failed'
    else:
        status = 'Failed'

    return status, slot_index


def SW(link, sw_width):
    sw_value = 0
    for r in range(0, len(link.linkslot) - sw_width + 1):
        if link.linkslot[r:r + sw_width] == [1] * sw_width:
            sw_value += 1
    print(sw_value)
    return sw_value

def SW_route(route, slot_width, sw_width):
    sw_value = 0
    for r in range(0, slot_width - sw_width + 1):
        sw_value += 1
        for link in route:
            if link.linkslot[r:r + sw_width] != [1] * sw_width:
                sw_value -= 1
                break

    #print(sw_value)

    return sw_value

def MPSW(node_s, node_d, all_node, all_link, slot_sum, tra_slot):
    route = []
    spt_node_d = node_d.copy()
    node_num = []
    link_length_num = []
    link_sw_num = []
    link_sw_dict = []
    #print('……………………MPSW Round 1……………………')
    o = 2
    (status, link_route, link_length) = SPT(node_s, all_node, all_link)#先找的源节点到各节点的最短路径
    for node in node_d:
        node_num.append(int(node.name))
        link_length_num.append(link_length[int(node.name)])
    link_length_dict = dict(zip(node_num, link_length_num))
    #print(link_length_dict)
    link_length_sorted = sorted(link_length_dict.items(), key=operator.itemgetter(1), reverse=False)
    #print(link_length_sorted)
    k = len(node_num)
    for i in range(0, k):
        #print(link_length_sorted[i])
        link_sw_dict.append(link_length_sorted[i][0])
        link_sw_num.append(SW_route(link_route[link_length_sorted[i][0]], slot_sum, tra_slot))
    link_sw = dict(zip(link_sw_dict, link_sw_num))
    #print(link_sw)
    link_sw_sored = sorted(link_sw.items(), key=operator.itemgetter(1), reverse=True)
    #print(link_sw_sored)
    index = link_sw_sored[0][0] - 1
    spt_node_d.remove(all_node[index])
    node_s.clear()
    node_s.append(all_node[index])
    #print(node_s[0])
    while len(spt_node_d) != 0:
        #print('……………………MPSW Round %d……………………' % o)
        o += 1
        spt_node_s = node_s.copy()
        link_length_num = []
        node_num = []
        #print(spt_node_s[d])
        (status, link_route_d, link_length_d) = SPT(spt_node_s, all_node, all_link)
        for node in spt_node_d:
            node_num.append(int(node.name))
            if link_length_d[int(node.name)] < link_length[int(node.name)]:
                link_length[int(node.name)] = link_length_d[int(node.name)]
                link_route[int(node.name)] = link_route_d[int(node.name)]
            link_length_num.append(link_length[int(node.name)])
        link_length_dict = dict(zip(node_num, link_length_num))
        #print(link_length_dict)
        link_length_sorted = sorted(link_length_dict.items(), key=operator.itemgetter(1), reverse=False)
        #print(link_length_sorted)
        link_sw_dict.clear()
        link_sw_num.clear()
        k = len(node_num)
        for i in range(0, k):
            #print(link_length_sorted[i])
            link_sw_dict.append(link_length_sorted[i][0])
            link_sw_num.append(SW_route(link_route[link_length_sorted[i][0]], slot_sum, tra_slot))
        link_sw = dict(zip(link_sw_dict, link_sw_num))
        #print(link_sw)
        link_sw_sored = sorted(link_sw.items(), key=operator.itemgetter(1), reverse=True)
        #print(link_sw_sored)
        index = link_sw_sored[0][0] - 1
        spt_node_d.remove(all_node[index])
        node_s.clear()
        node_s.append(all_node[index])
        #print('…………………………剩余节点……………………')
        #for g in range(0, len(spt_node_d)):
        #    print(spt_node_d[g])
    #print('~~~~~~~~~~~~~~~~~~路由链路~~~~~~~~~~~~~~~~~~~')
    for node in node_d:
        for k in range(0, len(link_route[int(node.name)])):
            #print(link_route[int(node.name)][k])
            route.append(link_route[int(node.name)][k])

    return route

def SWP_MPH(node_s, node_d, all_node, all_link, slot_sum, tra_slot):
    swp_link = []
    status = 'Failed'
    route = []
    slot_index = 0
    for i in range(slot_sum):
        mph_node_s = node_s.copy()
        mph_node_d = node_d.copy()
        swp_link = []
        for link in all_link:
            if link.linkslot[i:i + tra_slot] == [1] * tra_slot:
                swp_link.append(link)
        if len(swp_link) != 0:
            status, route = MPH(mph_node_s, mph_node_d, all_node, swp_link)
            status, slot_index = First_Fit(route, tra_slot, slot_sum)
            if status == 'Successful':
                return status, route, slot_index

    return status, route, slot_index


def poisson_arrive(lam, length):
    # 1/lam为单位时间（1）内的次数
    # length为单位时间个数
    # 即总个数为1/lam *length
    poisson_time = [0] * lam * length
    for index in range(0, length * lam):
        poisson_time[index] = poisson_time[index - 1] + np.random.exponential(scale=1/lam, size=None)  # 泊松到达
    #print(poisson_time)  # 泊松到达
    # a = [0] * length
    # for i in range(0, length):
    #    for item in poisson_time:
    #        if item < i + 1 and item >= i:
    #            a[i] += 1
    #    print('时间%d: %d' % (i, a[i]))  # 直方图可以看出是泊松分布
    # print(len(a))

    return poisson_time


def uniform_int(begin, end, size):
    list_int = []
    for i in range(0, size):
        a = random.randint(begin, end)
        list_int.append(a)

    return list_int


def node_random(all_node, num, mindn, maxdn):
    source_node = []
    destination_node = []
    d_all_node = []
    for i in range(0, num):
        source_node.append(random.choice(all_node))
        d_all_node = all_node.copy()
        d_all_node.remove(source_node[i])
        destination_node.append(random.sample(all_node, random.randint(mindn, maxdn)))

    """
        for i in range(10):
        print('源节点：', source[i].name, end='\t')
        print('目的节点：', end='\t')
        for j in range(len(destination[i])):
            print(destination[i][j].name, end='\t')
        print('\n')
    """

    return source_node,destination_node


def exp_working(lam, size):
    working_time = []
    for i in range(0, size):
        a = np.random.exponential(scale=lam, size=None)
        working_time.append(a)

    return working_time


def main():
    node_1 = Node('1', ['2', '3', '8'])
    node_2 = Node('2', ['1', '3', '4'])
    node_3 = Node('3', ['1', '2', '6'])
    node_4 = Node('4', ['2', '5', '9'])
    node_5 = Node('5', ['4', '6', '7'])
    node_6 = Node('6', ['3', '5', '13', '14'])
    node_7 = Node('7', ['5', '8', '14'])
    node_8 = Node('8', ['1', '7', '11'])
    node_9 = Node('9', ['4', '10', '12'])
    node_10 = Node('10', ['9', '11', '13'])
    node_11 = Node('11', ['8', '10', '12', '14'])
    node_12 = Node('12', ['9', '11', '13'])
    node_13 = Node('13', ['6', '10', '12'])
    node_14 = Node('14', ['6', '7', '11'])
    all_node = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, \
                node_8, node_9, node_10, node_11, node_12, node_13, node_14]

    slot_length = 320
    link1_2 = Link('1-2', [node_1, node_2], 1050, [1] * slot_length)
    link1_3 = Link('1-3', [node_1, node_3], 1500, [1] * slot_length)
    link1_8 = Link('1-8', [node_1, node_8], 2400, [1] * slot_length)
    link2_3 = Link('2-3', [node_2, node_3], 600, [1] * slot_length)
    link2_4 = Link('2-4', [node_2, node_4], 750, [1] * slot_length)
    link3_6 = Link('3-6', [node_3, node_6], 1800, [1] * slot_length)
    link4_5 = Link('4-5', [node_4, node_5], 600, [1] * slot_length)
    link4_9 = Link('4-9', [node_4, node_9], 1950, [1] * slot_length)
    link5_6 = Link('5-6', [node_5, node_6], 2400, [1] * slot_length)
    link5_7 = Link('5-7', [node_5, node_7], 600, [1] * slot_length)
    link6_13 = Link('6-13', [node_6, node_13], 1800, [1] * slot_length)
    link6_14 = Link('6-14', [node_6, node_14], 1050, [1] * slot_length)
    link7_8 = Link('7-8', [node_7, node_8], 750, [1] * slot_length)
    link7_14 = Link('7-14', [node_7, node_14], 1350, [1] * slot_length)
    link8_11 = Link('8-11', [node_8, node_11], 750, [1] * slot_length)
    link9_10 = Link('9-10', [node_9, node_10], 600, [1] * slot_length)
    link9_12 = Link('9-12', [node_9, node_12], 750, [1] * slot_length)
    link10_11 = Link('10-11', [node_10, node_11], 300, [1] * slot_length)
    link10_13 = Link('10-13', [node_10, node_13], 300, [1] * slot_length)
    link11_12 = Link('11-12', [node_11, node_12], 300, [1] * slot_length)
    link11_14 = Link('11-14', [node_11, node_14], 750, [1] * slot_length)
    link12_13 = Link('12-13', [node_12, node_13], 150, [1] * slot_length)
    all_link = [link1_2, link1_3, link1_8, link2_3, link2_4, link3_6, link4_5, link4_9, \
                link5_6, link5_7, link6_13, link6_14, link7_8, link7_14, link8_11, \
                link9_10, link9_12, link10_11, link10_13, link11_12, link11_14, link12_13]
    node_s = [node_1]
    node_d = [node_4, node_3]

    #route, length = SPT(node_s, all_node, all_link)             # MPH链路集合
    #for k in range(0, len(route)):
    #    print(route[k])

    #tra1 = Traffic('1', node_s, node_d, 5, 0, 0, route, [], 'Waiting')
    #MPSW(node_s, node_d, all_node, all_link)

    for u in range(1):
        print(u)
        arrive_time = poisson_arrive(20, 500)
        working_time = exp_working(5, 10000)
        end_time = [i + j for i, j in zip(arrive_time, working_time)]
        time_index = sorted(arrive_time + end_time)
        source, destination = node_random(all_node, 10000, 3, 8)
        tra_slot = uniform_int(1, 8, 10000)

        start = datetime.datetime.now()
        status = []
        source_node = []
        slot_dict = {}
        route_rom = [[] * 10000 for _ in range(10000)]

        for time in time_index:
            if time in arrive_time:
                tra_index = arrive_time.index(time)
                source_node.append(source[tra_index])
                destination_node = destination[tra_index].copy()
                # route = MPSW(source_node, destination_node, all_node, all_link, slot_length, tra_slot[tra_index])
                status_a, route = MPH(source_node, destination_node, all_node, all_link)
                route_rom[tra_index] = [m.name for m in route]
                status_a, slot_index = First_Fit(route, tra_slot[tra_index], slot_length)
                status.append(status_a)
                source_node.clear()
                slot_dict[tra_index] = slot_index
            else:
                tra_index = end_time.index((time))
                for link in all_link:
                    if link.name in route_rom[tra_index]:
                        link.linkslot[slot_dict[tra_index]:slot_dict[tra_index] + tra_slot[tra_index]] = [1] * tra_slot[
                            tra_index]
                del slot_dict[tra_index]
            # print(tra_index)

        #print(status)
        print('MPH')
        print('成功数：', status.count('Successful'))
        print('失败数：', status.count('Failed'))
        end = datetime.datetime.now()
        print('Running time: %s ' % (end - start))

        start = datetime.datetime.now()
        status = []
        source_node = []
        slot_dict = {}
        route_rom = [[] * 10000 for _ in range(10000)]

        for time in time_index:
            if time in arrive_time:
                tra_index = arrive_time.index(time)
                source_node.append(source[tra_index])
                destination_node = destination[tra_index].copy()
                route = MPSW(source_node, destination_node, all_node, all_link, slot_length, tra_slot[tra_index])
                #status_a, route = MPH(source_node, destination_node, all_node, all_link)
                route_rom[tra_index] = [m.name for m in route]
                status_a, slot_index = First_Fit(route, tra_slot[tra_index], slot_length)
                status.append(status_a)
                source_node.clear()
                slot_dict[tra_index] = slot_index
            else:
                tra_index = end_time.index((time))
                for link in all_link:
                    if link.name in route_rom[tra_index]:
                        link.linkslot[slot_dict[tra_index]:slot_dict[tra_index] + tra_slot[tra_index]] = [1] * tra_slot[
                            tra_index]
                del slot_dict[tra_index]
            # print(tra_index)

        # print(status)
        print('MPSW')
        print('成功数：', status.count('Successful'))
        print('失败数：', status.count('Failed'))
        end = datetime.datetime.now()
        print('Running time: %s ' % (end - start))

        start = datetime.datetime.now()
        status = []
        source_node = []
        slot_dict = {}
        route_rom = [[] * 10000 for _ in range(10000)]
        for time in time_index:
            if time in arrive_time:
                tra_index = arrive_time.index(time)
                source_node.append(source[tra_index])
                destination_node = destination[tra_index].copy()
                status_a, route, slot_index = SWP_MPH(source_node, destination_node, all_node, all_link, slot_length, tra_slot[tra_index])
                #route = MPSW(source_node, destination_node, all_node, all_link, slot_length, tra_slot[tra_index])
                #route = MPH(source_node, destination_node, all_node, all_link)
                route_rom[tra_index] = [m.name for m in route]
                #status_a, slot_index = First_Fit(route, tra_slot[tra_index], slot_length)
                status.append(status_a)
                source_node.clear()
                slot_dict[tra_index] = slot_index
            else:
                tra_index = end_time.index((time))
                for link in all_link:
                    if link.name in route_rom[tra_index]:
                        link.linkslot[slot_dict[tra_index]:slot_dict[tra_index] + tra_slot[tra_index]] = [1] * tra_slot[tra_index]
                del slot_dict[tra_index]
            #print(tra_index)
        print('SWP-MPH')
        print('成功数：', status.count('Successful'))
        print('失败数：', status.count('Failed'))
    # print(arrive_time)
    # print(working_time)
    # print(end_time)
    # print(time_index)
    end = datetime.datetime.now()
    print('Running time: %s ' % (end - start))


    print('hello')


if __name__ == '__main__':
    main()
