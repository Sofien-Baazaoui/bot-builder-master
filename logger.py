import inspect
import json


def pretty_log(function_name, args):
    """
    Pretty prints <dict>
    Each argument is in a new line.
    :param function_name: name of the function being logged
    :param args: arguments to be logged
    :return: None
    """
    print("=" * 100)
    print(" " * 40 + "In function: " + function_name + "()")
    print("-" * 100)
    for arg in args:
        if isinstance(arg, dict):
            print(json.dumps(arg, indent=4))
        else:
            print(arg)
        print("")
    print("=" * 100)

def generic_log(function_name, args):
    """
    Each variable is space separated.
    :param function_name: name of the function being logged
    :param args: arguments to be logged
    :return: None
    """
    print("*" * 100)
    print("function: " + function_name + "()")
    print(' '.join([str(arg) for arg in args]))
    print("*" * 100)


def log(pretty=False):
    """
    A curried function because:
    1. pretty is an positional argument
    2. *args needs to be second argument

    To keep pretty as separate set of arguments, function curries are used.

    Use as:
    ====================================
    log()(a, b, c) -> Generic logger
        or
    log(True)(a, b, c) -> Pretty logger
    ====================================

    :param pretty: Boolean, [default=False]
    :return: <function>
    """
    frame = inspect.currentframe()
    function_name = inspect.getouterframes(frame, 2)[1][3]
    def curried_printer(*args):
        """
        Has the context of function_name and pretty from the parent function (log in this case)
        :param args: list of arguments to be printed
        :return: <str>
        """
        if pretty:
            pretty_log(function_name, args)
        else:
            generic_log(function_name, args)
        return function_name
    return curried_printer
