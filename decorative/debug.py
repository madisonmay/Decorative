"""
Decorator for logging function inputs and outputs
"""
import inspect

from decorator import decorator


@decorator
def debug(fn, *args, **kwargs):
    """
    Log the inputs and ouptus of function `fn` to stdout

    Example usage:

    ```
    @debug
    def f(a, b):
        return a + b

    f(1, 2)
    f(3, 4)
    ```

    Stdout:
    ```
    f(a=1, b=2) --> 3
    f(a=3, b=4) --> 7
    ```
    """
    keyword_arguments = inspect.getcallargs(fn, *args, **kwargs)
    argument_string = ", ".join([
        "{0}={1}".format(k, v) for k, v in keyword_arguments.iteritems()
    ])
    result = fn(**keyword_arguments)
    print("{0}({1}) --> {2}".format(fn.__name__, argument_string, result))
    return result
