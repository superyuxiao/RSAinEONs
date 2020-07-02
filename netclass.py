class DisjointSet(dict):
    '''
    不相交集
    利用字典构成一个类似C语言中的链表结构，此举可以避免链路形成闭环
    '''

    def __init__(self, dict):
        pass

    def add(self, item):
        self[item] = item

    def find(self, item):
        if self[item] != item:
            self[item] = self.find(self[item])
        return self[item]

    def unionset(self, item1, item2):
        self[item2] = self[item1]

# 节点类
class Node(object):

    """
    :param name:节点名称
    :param con_node：与节点相连的其他节点
    """

    def __init__(self, name, con_node):
        self._name = name
        self._con_node = con_node

    @property
    def name(self):
        return self._name

    @property
    def con_node(self):
        return self._con_node

    @con_node.setter
    def con_node(self, con_node):
        self._con_node = con_node

    def __str__(self):
        return '节点%s'%self._name+',相邻节点%s'%self._con_node

#链路类
class Link(object):
    """
    :param name:链路名（编号）
    :param ternode:两端节点
    :param linkdistance:链路距离
    :param linkslot:链路频隙
    """
    def __init__(self, name, ternode, linkdistance, linkslot):
        self._name = name
        self._ternode = ternode
        self._linkdistance = linkdistance
        self._linkslot = linkslot

    @property
    def name(self):
        return self._name

    @property
    def ternode(self):
        return self._ternode

    @property
    def linkdistance(self):
        return self._linkdistance

    @property
    def linkslot(self):
        return self._linkslot

    @ternode.setter
    def ternode(self, node):
        self._ternode = node


    @linkdistance.setter
    def linkdistance(self, distance):
        self._linkdistance = distance

    @linkslot.setter
    def linkslot(self, slot):
        self._linkslot = slot

    #调制格式 BPSK QPSK 8QAM 16QAM
    #调制等阶 1，2，3，4
    def modformal(self):
        if self._linkdistance >= 4000:
            mod = 1
        elif self._linkdistance < 4000 and self._linkdistance >= 2000:
            mod = 2
        elif self._linkdistance < 2000 and self._linkdistance >= 1000:
            mod = 3
        else :
            mod = 4
        return mod

    def __str__(self):
        list_ternode = []
        for i in range(0,len(self._ternode)):
            list_ternode.append(self._ternode[i].name)
        return '链路'+'%s'%self._name+'，两端节点%s，链路距离%d，调制等阶%d，链路频隙%s'\
        %(list_ternode, self._linkdistance, self.modformal(), self._linkslot[:])

#业务类
class Traffic(object):
    """
    :param name:业务名（编号）
    :param source:源节点
    :param destination:目的节点
    :param traslot:占用频隙
    :param starttime:起始时间
    :param time:持续时间
    """
    def __init__(self, name, source, destination, traslot, starttime, time, alink, aslot, status):
        self._name = name
        self._source = source
        self._destination = destination
        self._traslot = traslot
        self._starttime = starttime
        self._time = time
        self._alink = alink
        self._aslot = aslot
        self._status = status

    @property
    def name(self):
        return self._name

    @property
    def source(self):
        return self._source

    @property
    def destination(self):
        return self._destination

    @property
    def traslot(self):
        return self._traslot

    @property
    def starttime(self):
        return self._starttime

    @property
    def time(self):
        return self._time

    @property
    def alink(self):
        return self._alink

    @property
    def aslot(self):
        return self._aslot

    @property
    def  status(self):
        return self._status

    @source.setter
    def source(self, nodes):
        self._source = nodes

    @destination.setter
    def destination(self, nodes):
        self._destination = nodes

    @traslot.setter
    def traslot(self, slot):
        self._traslot = slot

    @starttime.setter
    def starttime(self, time):
        self._starttime = time

    @time.setter
    def time(self, time):
        self._time = time

    @alink.setter
    def alink(self, alink):
        self._alink = alink

    @status.setter
    def status(self, status):
        self._status = status

    def __str__(self):
        list_destination = []
        for i in range(0,len(self._destination)):
            list_destination.append(self._destination[i].name)
        list_alink = []
        for i in range(0,len(self._alink)):
            list_alink.append(self._alink[i].name)
        return '业务'+'%s'%self._name+'，'+'源节点%s，'%self._source[0].name+'目的节点%s，'%sorted(list_destination)+\
               '占用频隙%d，起始时间%d，持续时间%d，\n  分配链路%s，分配频隙%s, 业务状态%s'\
        %(self._traslot, self._starttime, self._time, sorted(list_alink), sorted(list(self._aslot)), self._status)
