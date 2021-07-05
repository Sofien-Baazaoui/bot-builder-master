class Node(object):
    """
    A node instance contains a list of: next and previous nodes.
    The basic unit of a Graph data structure.
    """
    def __init__(self, name, data, nxt, pre, media, attribute):
        """
        :param name: <str>
        :param data: <object>
        :param nxt: <list>
        :param pre: <list>
        """
        self.name = name
        self.data = data
        self.nxt = nxt
        self.pre = pre
        self.media = media
        self.attribute = attribute

    def addNext(self, nxt):
        """
        :param nxt: new route to be added next to this node
        :return: this instance
        """
        self.nxt.append(nxt)
        return self

    def addPre(self, pre):
        """
        :param pre: new route to be added previous to this node
        :return: self
        """
        self.nxt.append(pre)
        return self

    def getCurrent(self):
        """
        :return: name of the current node
        """
        return self.name

    def getNext(self, fn):
        """
        :param fn: sorter function which accepts a list as an argument
        :return: one item from the list
        """
        return fn(self.nxt)