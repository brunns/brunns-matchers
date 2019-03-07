# encoding=utf-8
import logging
import random
import string
import sys
from inspect import isclass
from types import MethodType

logger = logging.getLogger(__name__)


def a_string(length=10, characters=string.ascii_letters + string.digits):
    return "".join(random.choice(characters) for _ in range(length))


def an_integer(a=None, b=None):
    return random.randint(a if a else 0, b if b else sys.maxsize)


def a_boolean():
    return one_of(True, False)


def one_of(*args):
    return random.choice(args)


class _BuilderMeta(type):
    def __new__(metacls, name, bases, namespace, **kwds):  # noqa: C901
        target = namespace.pop("target", None)
        args = namespace.pop("args", lambda: [])

        def __init__(self, **kwargs):
            # Defaults from factories (plus method overrides.
            for name, value in namespace.items():
                if name in {"build"}:  # It's an overridable base method.
                    m = MethodType(value, self)
                    setattr(self, name, m)
                elif isclass(value) and issubclass(value, Builder):  # It's a nested builder.
                    setattr(self, name, value().build())
                elif not name.startswith("__"):  # It's a field factory.
                    setattr(self, name, value())

            # Values from keyword arguments.
            for name, value in kwargs.items():
                setattr(self, name, value)

            self.args = args()

        def __getattr__(self, item):
            """Dynamic 'with_x' methods."""
            name = item.partition("with_")[2]
            if name:

                def with_(value):
                    setattr(self, name, value)
                    return self

                return with_

        def build(self):
            state = vars(self)
            args = state.pop("args", [])
            if callable(target):
                return target(*args, **state)
            else:
                raise ValueError("Needs a callable factory.")

        result = type.__new__(metacls, name, bases, {})

        setattr(result, __init__.__name__, __init__)
        setattr(result, __getattr__.__name__, __getattr__)
        setattr(result, build.__name__, build)

        return result


class Builder(metaclass=_BuilderMeta):
    target = None
