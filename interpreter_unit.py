import requests
import json
from commons.logger import log


def create_payload(query, state):
    if state["data"]["quick_replies"]:
        return {
            "query": {
                "text": query,
                "quick_replies": state["data"]["quick_replies"]
            }
        }
    else:
        return {

        }


def select_correct_payload(state):
    quick_replies = state["data"]["quick_replies"]

    for qr in quick_replies:
        if qr.get('title').replace(' ', '') == 'correct':
            return qr


class InterpreterResult(object):
    """
    Class for Interpreter result attributes
    """

    def __init__(self, result):
        self.result = result.get('result')
        self.intent = self.result.get('intent')
        self.entities = self.result.get('entities')
        self.sentiment = self.result.get('sentiment')
        self.query = self.result.get('query')
        self.small_talk = self.result.get('small_talk')


class Interpreter(object):
    """
    Add all class instances which can derive meaning from text, eg: NLP, regex, spell-checkers etc.
    """

    def __init__(self):
        # TODO: Create base url
        self.nlp_api_endpoint = "http://ec2-176-34-18-206.ap-northeast-1.compute.amazonaws.com:3000/holoash/nlp/v0.1/"
        self.nlp_api_test_endpoint = "http://127.0.0.1:1302/holoash/nlp/v0.1/predict_intent"
        self.nlp_api_get_test_score_endpoint = "http://127.0.0.1:1302/holoash/nlp/v0.1/get_similarity_score"
        self.nlp_api_get_prod_score_endpoint = "http://ec2-176-34-18-206.ap-northeast-1.compute.amazonaws.com:3000/holoash/nlp/v0.1/get_similarity_score"

    def query(self, query):
        url = self.nlp_api_test_endpoint + "?query=" + query
        prediction = requests.request("GET", url)
        text = json.loads(prediction.text)
        log()(text)
        return InterpreterResult(text)

    def get_correct_payload(self, query, state):
        # payload = create_payload(query, state)
        payload = select_correct_payload(state)
        # url = self.nlp_api_get_test_score_endpoint
        # score = requests.post(url=url, json=payload)
        # result = json.loads(score.text)['result']
        log()(payload)
        return payload

    def get_similarity_score(self, query, state):
        # payload = create_payload(query, state)
        payload = select_correct_payload(state)
        # url = self.nlp_api_get_test_score_endpoint
        # score = requests.post(url=url, json=payload)
        # result = json.loads(score.text)['result']
        log()(payload)
        return payload


#
# interpreter = Interpreter()
# state =  {'session_name': 'get_name_session_4', 'current_node': 'ID1', 'data': {'quick_replies': [{'title': ' correct ', 'payload': 'ID2', 'content_type': 'text'}, {'title': ' incorrect', 'payload': 'ID3', 'content_type': 'text'}], 'text': ['Hi there, my name is Ashlee. What is your name? '], 'media': '', 'next': ('ID2,ID3',), 'attribute': 'name'}}
# query = "My name is James Bond"
# result = interpreter.query(query)
# print("result: ", result.entities.people)


