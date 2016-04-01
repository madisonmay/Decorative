"""
Decorator for runtime type checking
"""
import inspect

from decorator import decorator


class TypeCheckError(TypeError):
    pass


def typecheck(**type_map):
    """
    Ensure that all keyword arguments are of the desired types.
    Raises a TypeCheckError when invalid arguments are encountered

    Example usage:

    ```
    @typecheck(a=float, b=float)
    def divide(a, b):
        return a/b

    # Passing in multiple valid types for a single keyword argument is also valid

    @typecheck(a=(int, float), b=(int, float)):
    def divide(a, b):
        return float(a) / float(b)
    ```

    """
    @decorator
    def wrapper(fn, *args, **kwargs):
        keyword_arguments = inspect.getcallargs(fn, *args, **kwargs)
        for keyword, keyword_type in type_map.items():
            value = keyword_arguments.get(keyword)
            if not isinstance(value, keyword_type):
                raise TypeCheckError(
                    "Provided argument for `{}` keyword was not of type `{}`".format(
                        keyword, keyword_type
                    )
                )
        return fn(**keyword_arguments)
    return wrapper
