"""
This file serves as a map between a chat-node and the database function which provides data to the particular node.

    1. Functions must supply necessary data to evaluate <Template>
    2. Functions must return data in the specified format:

    ======================================================
    TEXT: <list dict>
    1.  template example:
        "text": ["Hello {{user}}"]

        expected return value: {
            "user": <value from source>
        }

    2. template example: {
            "text": ["We have {{...items}} for you]
        }

        expected return value: [{
            "...items": ["apples", "oranges]
        }]

    ... before a variable (...items) means an array is expected for its value.
    ======================================================
    QUICK_REPLIES: <list dict>
    template example:
        "quick_replies": {
          "iterable": {
            "type": "text",
            "title": "{{item_name}}",
            "payload": "{{item_tag}}"
          }
        }

    expected return value:
        [{
            "item_name": "Torch",
            "item_tag": "TORCH1NSB11"
        }, {
            "item_name": "Screwdriver",
            "item_tag": "SCREW1NSD13"
        }, ... ]

    ======================================================
    ATTACHMENTS: <dict>
    template example:
        "attachments": {
          "iterable": {
            "type": "template",
            "elements": {
              "title": "{{product_name}}",
              "image": "{{image_url}}",
              "buttons": [{
                  "title": "Add {{product_name}} to cart",
                  "type": "text",
                  "payload": "CART_IN?p_id={{product_id}}"
                },
                {
                  "title": "Remove {{product_name}} from cart",
                  "type": "text",
                  "payload": "CART_OUT?p_id={{product_id}}"
                }]
            }
          }
        }

    expected return value: {
        "type": "template",
        "elements: [{
            "product_name": "Torch",
            "image_url": "404 Not Found",
            "buttons": [{
                "product_name": "Torch",
                "product_id": "TORCH1NSB11"
            }, {
                "product_name": "Torch",
                "product_id": "TORCH1NSB11"
            }]
        }]
    }
    ======================================================
"""
import ast
import random
import datetime
import humanfriendly
from django.core.cache import cache
from constants import KEYS
import emoji
from commons.errors import ChatNodeNameTypeError
from commons.logger import log
from user.models import Profile


def add_emoji(**args):
    return [{
        "thinking_emoji": ''.join(emoji.emojize(':thinking_face:'))
    }]


def no_op(**args):
    return None


def do_small_talk(**args):
    log()(args)
    if args['small_talk']:
        small_talk = args['small_talk']\
            .replace('{{ first_name }}', '')\
            .replace('{{ happy_emoji }}', emoji.emojize(":grinning_face:") )
    else:
        small_talk = 'Hello there! ' + emoji.emojize(":grinning_face:")
    return [{
        "small_talk_text": small_talk
    }]


def attach_get_reminder_vars(**kwargs):
    sender_id = kwargs.get(KEYS.FB_ID)
    now = datetime.datetime.utcnow().timestamp()
    events_cached = cache.get(sender_id + '_reminder')
    if not events_cached:
        return [{ "reminder_text": "You don't have any reminders set." }]
    log()('events cached', events_cached, type(events_cached))
    all_events = ast.literal_eval(events_cached)
    if not all_events:
        return [{ "reminder_text": "You don't have any reminders set." }]
    log()(all_events)
    events = []
    if all_events:
        events = [{
            'name': event['name'],
            'datetime': float(event['datetime'])
        } for event in all_events if float(event['datetime']) > now]

    if not events:
        return [{ "reminder_text": "You don't have any reminders set." }]
    else:
        reminder_text = "Ok, the next thing(s) in line are: "
        for i, event in enumerate(events):
            date_time = datetime.datetime.fromtimestamp(event['datetime'])
            date_time_str = date_time.strftime("%Y-%m-%d %H:%M:%S")
            time_left = date_time - datetime.datetime.utcnow()
            time_left_str = humanfriendly.format_timespan(time_left)
            reminder_text += "{}) {} at {}, ({}) \n".format(
                i + 1,
                event.get('name', ''),
                date_time_str,
                time_left_str
            )
        return [{
            "reminder_text": reminder_text
        }]


def attach_set_reminder_vars(**kwargs):
    entities = kwargs.get(KEYS.ENTITIES)
    sender_id = kwargs.get(KEYS.FB_ID)
    time = entities.get(KEYS.TIME)
    date = entities.get(KEYS.DATE)
    query = kwargs.get(KEYS.QUERY)
    head = [
        "{emoji} Ha!",
        "{emoji} Alright!",
        "I've got your back!",
        "Cool!!",
        "Awesome!",
        "Sure thing!",
        "Why not!",
        "Anything for you buddy..",
        "Great! I got this..",
        "You know, I am perfect for this one thing?",
        "{emoji} Alright..",
        "{emoji} Will do buddy..",
        "I wont let you miss this."
    ]

    body = [
        "reminder: {date} {time} [event:{event}] ",
        "{date} {time} [event:{event}]",
        "this event at {date} {time} [event:{event}]",
        "reminder for {date} {time} [event:{event}]",
        "be ready {date} {time} [event:{event}]",
        "good luck {date} {time} [event:{event}]",
        "start preparing {date} {time} [event:{event}]",
    ]

    tail = [
        "is safe in my head",
        "is noted in my memory",
        "will be saved",
        "is saved",
        "is set",
        "goes into my hard-drive",
        "into the calendar",
        "saved in the calender",
        "saved",
        "noted."
    ]

    emoji_list = [
        emoji.emojize(':grinning_face:'),
        emoji.emojize(':face_with_tongue:'),
        emoji.emojize(':winking_face:'),
        emoji.emojize(':stopwatch:'),
        emoji.emojize(':hugging_face:'),
        emoji.emojize(':astonished_face:'),
        emoji.emojize(':hushed_face:'),
        emoji.emojize(':OK_hand:'),
        emoji.emojize(':victory_hand:'),
        emoji.emojize(':thumbs_up:'),
        emoji.emojize(':flexed_biceps:'),
        emoji.emojize(':rose:'),
        emoji.emojize(':four_leaf_clover:'),
        emoji.emojize(':alarm_clock:'),
        emoji.emojize(':glowing_star:'),
        emoji.emojize(':party_popper:'),
        emoji.emojize(':bell:'),
        emoji.emojize(':mobile_phone:'),
        emoji.emojize(':open_book:'),
        emoji.emojize(':green_book:'),
        emoji.emojize(':blue_book:'),
        emoji.emojize(':pencil:'),
        emoji.emojize(':briefcase:'),
        emoji.emojize(':white_heavy_check_mark:')
    ]

    reminder_text = "{head} {body} {tail} {emoji_1} {emoji_2}".format(
        head=random.choice(head),
        body=random.choice(body),
        tail=random.choice(tail),
        emoji_1=random.choice(emoji_list),
        emoji_2=random.choice(emoji_list)
    )

    timestamp = datetime.datetime.strptime('{} {}'.format(date, time),'%Y-%m-%d %H:%M:%S')
    datetime_format = timestamp.timestamp()
    events_str = cache.get(sender_id + '_reminder')

    log()(events_str, type(events_str))

    events = ast.literal_eval(events_str) if events_str != None else []
    event = {
        'name': query,
        'datetime': datetime_format
    }
    events.append(event)
    log()('stringified events', str(events))
    cache.set(sender_id + '_reminder', str(events))
    log()('read cache', cache.get(sender_id + '_reminder'))
    reminder_text = reminder_text.format(emoji=random.choice(emoji_list), date=date, time=time, event=query)

    return [{
        "reminder_text": reminder_text
    }]


def attach_quick_reply_vars(**kwargs):
    data = kwargs.get(KEYS.DATA)
    quick_replies       = data[KEYS.QUICK_REPLIES]

    return []


def attach_quick_reply_options(**kwargs):
    data = kwargs.get(KEYS.DATA)
    collection = data[KEYS.COLLECTION]
    chat_graph = kwargs.get(KEYS.CHAT_GRAPH)

    def create_collection(sessions):
        collection = []
        for idx in range(len(sessions)):
            session_name = sessions[idx]
            collection.append({
                "title": chat_graph.get_session_title(session_name),
                "payload": session_name,
                "content_type": "text"
            })
        return collection

    return create_collection(collection)


def attach_text_reply_vars(**kwargs):
    fb_id           = kwargs.get(KEYS.FB_ID)
    profile         = Profile.get_profile_data(fb_id)

    return [profile.metadata]


node_function_map = {
    'SMALL_TALK': {
        "txt": do_small_talk,
        "qr": no_op,
        "at": no_op
    },
    'GET_REMINDER': {
        "txt": attach_get_reminder_vars,
        "qr": no_op,
        "at": no_op
    },
    'SET_REMINDER': {
        "txt": attach_set_reminder_vars,
        "qr": no_op,
        "at": no_op
    },
    'show_options': {
        "txt": attach_text_reply_vars,
        "qr": attach_quick_reply_options,
        "at": no_op
    }
}


def function_data_map(node_name):
    """
    Returns a chat-node if found in chat-graph layout.
    :param node_name: <str>
    :return: <ChatNode>
    """
    if type(node_name) is not str:
        raise ChatNodeNameTypeError(node_name)
    elif node_name not in node_function_map:
        return {
            "txt": attach_text_reply_vars,
            "qr": attach_quick_reply_vars,
            "at": no_op
        }
    return node_function_map[node_name]
