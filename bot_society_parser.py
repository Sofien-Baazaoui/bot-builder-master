import pandas as pd
import json
from constants import PATHS
from web_tools.s3 import S3
from commons.logger import log


def is_nan(num):
    return num != num


class Interaction:
    """
    This class handles interaction data
    """

    def __init__(self, val):
        self.data          = val
        self.id            = self._get_id()
        self.bot_utterance = self._get_split_text(self.data[0], operator='|')
        self.next_nodes    = self._get_next_nodes()
        self.quick_replies = self._get_quick_replies()
        self.split_text    = self._get_split_text(self.bot_utterance[0], operator=':')
        self.text          = self._get_text()
        self.attribute     = self._get_attribute()
        self.media         = self._get_media()

    def get_instance(self):
        """
        Function which returns the current instance
        :return: dict
        """
        return {
            'id': self.id,
            'text': [self.text],
            'media': self.media,
            'quick_replies': self.quick_replies,
            'next': self.next_nodes,
            'pre': self.id,
            'attribute': self.attribute
        }

    def _get_id(self):
        """
        :return: string
        """
        return self.data[4]

    def _get_text(self):
        """
        :return: string
        """
        return self.split_text[0]

    def _get_split_text(self, data, operator):
        """
        :return:
        """
        return data.split(operator)

    def _get_quick_replies(self):
        """
        :return:
        """
        qr = self.bot_utterance[1:]

        return self._add_quick_replies(qr) if qr != [] else []

    def _get_media(self):
        """
        :return:
        """
        return "" if is_nan(self.data[3]) else self.data[3]

    def _get_attribute(self):
        """
        Function which returns an attribute which is to be captured
        as part of this interaction
        :return: string
        """
        return self.split_text[1] if len(self.split_text) > 1 else ""

    def _get_next_nodes(self):
        """
        Function which returns the required next nodes of the current interaction
        :return: string
        """
        next_nodes = self.data[5] if not is_nan(self.data[5]) else "eos"
        if is_nan(next_nodes):
            next_nodes = "eos"
        return next_nodes

    def _add_quick_replies(self, qr):
        """
        Function to set quick replies payload
        :param qr:
        :return:
        """
        result = list()
        next_nodes = self.next_nodes.split(",")

        for idx, quick_reply in enumerate(qr):
            result.append({
                "title": quick_reply,
                'payload': next_nodes[idx],
                'content_type': "text"
            })

        return result


class ScriptParser:
    """
    The purpose of the class is to read a session script (csv export from bot society)
    as input and add it to the session config.
    """

    def __init__(self, input_file, session_name, session_title):
        self.input_df           = pd.read_csv(input_file)
        self.session_name       = session_name
        self.session_title      = session_title
        self.config             = S3().get_item_from_s3('holobot_new.json')
        self.interactions       = []

    def add_session_interactions(self):
        """
        Function to create interactions for each session
        :return:
        """
        for i, val in enumerate(self.input_df.values):
            if i == 0:
                # skip first record and
                continue # forward
            interaction = Interaction(val).get_instance()

            self.interactions.append({
                'name': interaction.get('id'),
                'text': interaction.get('text'),
                'media': interaction.get('media'),
                'quick_replies': interaction.get('quick_replies'),
                'next': interaction.get('next'),
                'pre': interaction.get('id'),
                'attribute': interaction.get('attribute')
            })

        return self.interactions

    def add_session_to_config(self):
        """
        :return:
        """

        self.config[self.session_name] = {
                "session_title":    self.session_title,
                "interactions":     self.add_session_interactions()
            }

        with open(PATHS.holobot_config_path, "w") as json_out_file:
            json.dump(self.config, json_out_file, indent=2)

        S3().set_item_in_s3('holobot_new.json', PATHS.holobot_config_path)
        log()("Session <{}> added to config".format(self.session_name))

    def session_exists_in_config(self):
        """
        :return:
        """
        return self.session_name in self.config.keys()

    def add_session(self):
        """
        :return:
        """
        if not self.session_exists_in_config():
            self.add_session_to_config()
        else:
            log()("Session <{}> already exists in config".format(self.session_name))
