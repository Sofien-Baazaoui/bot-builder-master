
from web_tools.s3 import S3
from commons.logger import log


class SessionGraph:

    def __init__(self):
        self.session_graph = S3().get_item_from_s3("session_graph.json")
        # log()("Reading session graph from config: ", self.session_graph)

    def get_instance(self):
        return self.session_graph

    def get_sessions(self, session_key):
        return self.session_graph[session_key] \
            .strip("[]") \
            .replace("'", "") \
            .replace(" ", "") \
            .split(',')
