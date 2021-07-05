class ChatNodeNotFound(Exception):
    """
    Raise if node_name not found while searching in a chat-graph.
    """
    def __init__(self, invalid_node):
        self.message = str(invalid_node) + " is not present in the chat-layout."
        super(ChatNodeNotFound, self).__init__(self.message)

class ChatNodeNameTypeError(TypeError):
    """
    Raise when chat-node name provided for node-search operations is not a string.
    """
    def __init__(self, unhandled_type):
        self.message =  "Node name: "+ str(unhandled_type) + " should have been a string."

class InsufficientItemsQuery(Exception):
    """
    Raise when a database call doesn't provide adequate results
    """
    def __init__(self):
        self.message = "No items retrieved from the database."
        super(InsufficientItemsQuery, self).__init__(self.message)

class InsufficientLocationsQuery(Exception):
    """
    Raise when a query doesn't provide adequate locations
    """
    def __init__(self):
        self.message = "No items retrieved from the database."
        super(InsufficientLocationsQuery, self).__init__(self.message)

class IntentAPIError(Exception):
    """
    Raise when intents' API (located in interpreter) results in an error
    """
    def __init__(self, error_code, query):
        if error_code[0] == "4":
            # 4XX error series, maps to verify_app-using client
            self.message = "Invalid use of Intent's API for query: %s, query_type: %s" % (query, type(query))
        elif error_code[1] == "5":
            # 5XX error series, maps to internal errors in the verify_app
            self.message = "The endpoint failed to respond for query: %s" % query