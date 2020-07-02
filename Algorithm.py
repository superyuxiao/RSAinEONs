from netclass import DisjointSet

def MST(node, link):
    """
    :param node:节点
    :param link:链路
    :return:最小生成树的链路
    节点必须是相邻的
    """
    MST = []
    edges = sorted(link, key=lambda link: link.linkdistance)
    # 排序后链路
    for i in range(0, len(link)):
        print(edges[i])
    nodes = []
    for i in range(0, len(node)):
        nodes.append(node[i].name)
    forest = DisjointSet(nodes)
    for item in nodes:
        forest.add(item)
    print(forest) #节点字典
    num_sides = len(nodes) - 1  # 最小生成树的边数等于顶点数减一
    for e in edges:
        node1 = e.ternode[0].name
        node2 = e.ternode[1].name
        parent1 = forest.find(node1)
        parent2 = forest.find(node2)
        if parent1 != parent2:
            MST.append(e)
            print('添加', e)
            num_sides -= 1
            if num_sides == 0:
                return MST
            else:
                forest.unionset(parent2, parent1)

def SPT(node_s, all_node, all_link):
    """
    :param node_s:起始源节点 list格式
    :param all_node: 所有节点集合
    :param all_link: 所有链路集合
    :return: link_route指向其余各节点的路由 link_length各最短路径的长度
    """
    status = 'Successful'
    length = len(all_node)
    length += 2
    node_d = all_node.copy()
    for v in range(0, len(node_s)):
        node_d.remove(node_s[v])
    node_box = []
    #print(length)
    link_route = [[] * length for _ in range(length)]
    link_length = [99999] * length
    link_length[int(node_s[0].name)] = 0
    i = 1
    while len(node_d) != 0:
        #print('…………Round %d…………' % i)
        for link in all_link:
            if link.ternode[0] in node_s and link.ternode[1] in node_d:
                #print('0', link)
                node_box.append(link.ternode[1])
                last_length = link_length[int(link.ternode[0].name)] + link.linkdistance
                #print('last length %d' % last_length)
                #print(int(link.ternode[1].name))
                if link_length[int(link.ternode[1].name)] > last_length:
                    link_length[int(link.ternode[1].name)] = last_length
                    link_route[int(link.ternode[1].name)].clear()
                    link_route[int(link.ternode[1].name)] += link_route[int(link.ternode[0].name)]
                    link_route[int(link.ternode[1].name)].append(link)
            if link.ternode[0] in node_d and link.ternode[1] in node_s:
                #print('1', link)
                node_box.append(link.ternode[0])
                last_length = link_length[int(link.ternode[1].name)] + link.linkdistance
                #print('last length %d' % last_length)
                #print(int(link.ternode[0].name))
                if link_length[int(link.ternode[0].name)] > last_length:
                    link_length[int(link.ternode[0].name)] = last_length
                    link_route[int(link.ternode[0].name)].clear()
                    link_route[int(link.ternode[0].name)] += link_route[int(link.ternode[1].name)]
                    link_route[int(link.ternode[0].name)].append(link)
        for j in range(0, len(node_box)):
            node_s.append(node_box[j])
            if node_d.count(node_box[j]) > 0:
                node_d.remove(node_box[j])
            #print(node_box[j])
        node_box.clear()
        i += 1
        if i > 10 :
            status = 'Failed'
            return status, link_route, link_length
    #for l in range(0, len(link_route[10])):
    #    print(link_route[10][l])
    #print(link_length[10])

    return status, link_route, link_length

def MPH(node_s, node_d, all_node, all_link):
    status = 'Successful'
    route = []
    spt_node_d = node_d.copy()
    #print('……………………MPH Round 1……………………')
    o = 2
    (status, link_route, link_length) = SPT(node_s, all_node, all_link)#先找的源节点到各节点的最短路径
    if status == 'Failed':
        return status, route
    short_node_length = link_length[int(node_d[0].name)]       #并找到其中最短的一个，加入到源节点集合中
    index = int(node_d[0].name)
    for node in spt_node_d:
        if short_node_length > link_length[int(node.name)]:
            short_node_length = link_length[int(node.name)]
            index = int(node.name)                              #索引
    index -= 1
    spt_node_d.remove(all_node[index])
    node_s.clear()
    node_s.append(all_node[index])                              #对刚刚纳入源节点集合的节点进行SPT
    while len(spt_node_d) != 0:
        #print('……………………MPH Round %d……………………' % o)
        o += 1
        spt_node_s = node_s.copy()
        #for d in range(0, len(spt_node_s)):
        #    print(spt_node_s[d])
        (status, link_route_d, link_length_d) = SPT(spt_node_s, all_node, all_link)
        if status == 'Failed':
            return status, route
        short_node_length = link_length_d[int(spt_node_d[0].name)]
        index = int(int(spt_node_d[0].name))
        for node in spt_node_d:
            if link_length_d[int(node.name)] < link_length[int(node.name)]:
                link_length[int(node.name)] = link_length_d[int(node.name)]
                link_route[int(node.name)] = link_route_d[int(node.name)]
            if short_node_length > link_length[int(node.name)]:
                short_node_length = link_length[int(node.name)]
                index = int(node.name)
        index -= 1
        spt_node_d.remove(all_node[index])
        node_s.clear()
        node_s.append(all_node[index])
        #print('…………………………剩余节点……………………')
        #for g in range(0, len(spt_node_d)):
            #print(spt_node_d[g])
    #print('~~~~~~~~~~~~~~~~~~路由链路~~~~~~~~~~~~~~~~~~~')
    for node in node_d:
        for k in range(0, len(link_route[int(node.name)])):
            #print(link_route[int(node.name)][k])
            route.append(link_route[int(node.name)][k])

    return status, route

def selectlink(set_node, all_link):
    """
    :param set_node: 给定节点
    :param all_link: 所有链路
    :return: 两端节点都属于给定节点集合的链路
    """
    set_link = []
    for link in all_link:
        if link.ternode[0] in set_node and link.ternode[1] in set_node:
            set_link.append(link)
    return set_link