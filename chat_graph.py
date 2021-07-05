from core.chat_node.chat_node import ChatNode
from commons.errors import ChatNodeNameTypeError, ChatNodeNotFound

from messenger.utils.response.ResponseTypes.QuickReplyResponse import QuickReplyResponse


def setup_data(obj):
    """
    1. Extracts text, quick replies, attachments from object
    2. Adds available entities to a dict and returns it
    :param obj: <dict>
    :return: <dict>
    """
    data = {}
    for prop in obj:
        if prop in ["text", "quick_replies", "attachments"]:
            data[prop] = obj[prop]
    return data


class Graph(object):
    """
    A graph which contains:
     1. chat-nodes in a layout; containing { node-name: node } as <dict>
     2. contains the start and end nodes for a chat instance.
    """

    def __init__(self, json):
        self.layout = {}
        self.out = {}
        self.json = json
        self.start = None
        self.end = None

    def get_node(self, node_name, session_name):
        """
        :param session_name: <str> should correspond to key in self.layout
        :param node_name:    <str> should correspond to key in self.layout.session_name
        :return: <ChatNode>
        """
        if type(node_name) is not str:
            raise ChatNodeNameTypeError(node_name)
        if node_name not in self.layout[session_name]:
            raise ChatNodeNotFound(node_name)
        return self.layout[session_name][node_name]["node"]

    def get_session_title(self, session_name):
        """
        :param session_name: <str> should correspond to key in self.layout
        :return: <ChatNode>
        """
        return self.layout[session_name]["title"]

    def node_in_graph(self, node_name):
        if type(node_name) is not str:
            raise ChatNodeNameTypeError(node_name)
        elif node_name in self.layout:
            return True
        else:
            raise ChatNodeNotFound(node_name)

    # def generate_quick_replies_from_template(self, sessions, session_name, current_node):
    #     return QuickReplyResponse(
    #         self.get_quick_reply_from_graph(session_name, current_node)
    #     ).eval(create_collection(self, sessions))

    def get_quick_reply_from_graph(self, session_name, current_node):
        return self.get_node(current_node, session_name).data.quick_replies

    def get_text_from_graph(self, session_name, current_node):
        return self.get_node(current_node, session_name).data.text

    def get_next_node_from_graph(self, session_name, current_node):
        return self.get_node(current_node, session_name).nxt

    def get_media_from_graph(self, session_name, current_node):
        return self.get_node(current_node, session_name).media

    def get_attribute_from_graph(self, session_name, current_node):
        return self.get_node(current_node, session_name).attribute

    def draw_graph(self):
        """
        sets up graph instance after reading json file
        """
        for idx, session in enumerate(self.json):
            interactions    = self.json[session]["interactions"]
            title           = self.json[session]["session_title"]

            out = {}
            for i in range(len(interactions)):
                prop        = interactions[i]
                nxt         = prop["next"] if "next" in interactions[i] else None
                pre         = prop["pre"] if "pre" in interactions[i] else None
                media       = prop["media"] if "media" in interactions[i] else None
                name        = prop["name"] if "name" in interactions[i] else None
                attribute   = prop["attribute"] if "attribute" in interactions[i] else None

                cn          = ChatNode(name, setup_data(interactions[i]), nxt, pre, media, attribute)

                out[name] = {
                    "node": cn
                }
                out["title"] = title

                if self.start is None:
                    self.start = cn
                self.end = cn

            self.layout[session] = out
