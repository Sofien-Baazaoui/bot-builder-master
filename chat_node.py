from core.node.node import Node
from messenger.utils.response.response import Response


class ChatNode(Node):
    """
    ChatNode, inherits Node Class,
    represents a node in a chat-flow
    """
    def __init__(self, name, data=None, nxt=None, pre=None, media=None, attribute=None):

        """
        :param name: <str>
        :param data: <object>
        :param nxt: <list>
        :param pre: <list>
        """
        if pre is None:
            pre = []
        if nxt is None:
            nxt = []
        if media is None:
            media = []
        if attribute is None:
            attribute = ""
        if data is not None:
            data = Response(data, nxt=nxt, media=media, attribute=attribute)
        super(ChatNode, self).__init__(name, data, nxt, pre, media, attribute)

