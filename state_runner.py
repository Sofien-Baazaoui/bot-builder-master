from django.core.cache import cache
from commons.logger import log
from constants import KEYS, PATHS
from core.state_runner.models import StateStore
from core.session_graph.session_graph import SessionGraph


class StateRunner(object):
    """
    This class is used for tracking and store the state of user chat sessions
    """

    def __init__(self, sender_id=None, chat_graph=None, message=None):
        # session_graph is used as a session orchestrator.
        self.session_graph = SessionGraph()
        self.sender_id = sender_id
        self.chat_graph = chat_graph
        self.starting_session = list(self.session_graph.get_instance().keys())[0]
        self.starting_node = KEYS.STARTING_NODE
        self.sessions = []
        self.interaction = ""
        self.session_name = ""
        self.collection = []
        self.payload = message.get(KEYS.ACTION) if message is not None else "" # contains either Interaction node
                                                                               # or Session name as payload value
        self.current_node = self.payload if self.payload not in self.session_graph.get_instance().keys() else ""
                                                                        #                                      ^
                                                                        # meaning session is sent back as payload

    def __get_current_interaction(self):
        """
        :return:
        """
        quick_replies = self.chat_graph\
            .get_quick_reply_from_graph(
                    self.session_name,
                    self.current_node)

        text = self.chat_graph\
            .get_text_from_graph(
                    self.session_name,
                    self.current_node)

        media = self.chat_graph\
            .get_media_from_graph(
                    self.session_name,
                    self.current_node)

        next_node = self.chat_graph\
            .get_next_node_from_graph(
                    self.session_name,
                    self.current_node),

        attribute = self.chat_graph\
            .get_attribute_from_graph(
                    self.session_name,
                    self.current_node)

        return {
            "quick_replies":    quick_replies,
            "text":             text,
            "media":            media,
            "next":             next_node,
            "attribute":        attribute,
            "collection":       self.collection
        }

    def __get_next_session(self):
        self.sessions = self.session_graph.get_sessions(self.session_name)

        if len(self.sessions) == 1:
            return self.sessions[0]  # set next session
        else:
            self.collection = self.sessions  # show options
            return KEYS.SHOW_OPTIONS

    def __get_session_starting_node(self):
        return self.starting_node  # self.chat_graph.layout[self.session_name][self.starting_node]["node"].nxt

    def __get_next_state(self):
        if self.current_node in ["eos"]:  # end of session
            self.session_name = self.__get_next_session()
            self.current_node = self.__get_session_starting_node()
            self.interaction = self.__get_current_interaction()
        elif self.current_node == "":  # meaning session is sent back as payload
            self.current_node = self.__get_session_starting_node()
            self.interaction = self.__get_current_interaction()

        else:
            self.interaction = self.__get_current_interaction()

        return self.current_instance()

    def __create_new_state(self):
        self.session_name = self.starting_session
        self.current_node = self.__get_session_starting_node()
        self.interaction = self.__get_current_interaction()

        return self.current_instance()

    def __create_new_instance(self):
        state = self.__create_new_state()
        cache.set(self.sender_id, state)
        state_store_db_obj = StateStore(sender_id=self.sender_id, state=state)
        state_store_db_obj.save()

        log()('New user {}, new state created: {}'.format(self.sender_id, state))
        return state

    def __create_next_instance(self):
        state = self.__get_next_state()
        print("state dump: ", state)
        cache.set(self.sender_id, state)
        state_store_db_obj = StateStore(sender_id=self.sender_id, state=state)
        state_store_db_obj.save()

        log()('Returning user {}, old state updated: {}'.format(self.sender_id, state))
        return state

    def __set_session_name_from_db(self):
        if self.payload in self.session_graph.get_instance().keys():
            self.session_name = self.payload
        else:
            self.session_name = StateStore.get_state_by_sender_id(self.sender_id).state[KEYS.SESSION_NAME]

    def __set_session_name_from_cache(self):
        if self.payload in self.session_graph.get_instance().keys():
            self.session_name = self.payload
        else:
            self.session_name = cache.get(self.sender_id)[KEYS.SESSION_NAME]

    def sender_id_exists_in_cache(self):
        """
        TODO Move this to the appropriate class
        :return:
        """
        return cache.__contains__(self.sender_id)

    def create_instance(self):
        if not self.sender_id_exists_in_cache():  # not in cache
            if not StateStore.sender_id_exists_in_db(self.sender_id):  # not in db
                return self.__create_new_instance()  # return from config
            else:  # return from db
                self.__set_session_name_from_db()
                return self.__create_next_instance()
        else:  # return from cache
            self.__set_session_name_from_cache()
            return self.__create_next_instance()

    def current_instance(self):
        return {
            "session_name": self.session_name,
            "current_node": self.current_node,
            "data": self.interaction
        }
