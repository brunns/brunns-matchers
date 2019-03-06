# encoding=utf-8
import logging
import random
import string
from inspect import isclass
from types import MethodType

logger = logging.getLogger(__name__)


def a_string(length=10, characters=string.ascii_letters + string.digits):
    return "".join(random.choice(characters) for _ in range(length))


def an_integer(a=None, b=None):
    return random.randint(a, b)


def a_boolean():
    return random.choice([True, False])


class _BuilderMeta(type):
    def __new__(metacls, name, bases, namespace, **kwds):  # noqa: C901
        target = namespace.pop("target", None)

        def __init__(self):
            for name, value in namespace.items():
                if name in {"build"}:  # It's an overridable base method.
                    m = MethodType(value, self)
                    setattr(self, name, m)
                elif isclass(value) and issubclass(value, Builder):  # It's a nested builder
                    setattr(self, name, value().build())
                elif not name.startswith("__"):  # It's a field factory.
                    setattr(self, name, value())

        def __getattr__(self, item):
            """Dynamic 'with_x' methods."""
            name = item.partition("with_")[2]
            if name:

                def with_(value):
                    setattr(self, name, value)
                    return self

                return with_

        def __getitem__(self, item):
            return self.value[item]

        def build(self):
            if callable(target):
                return target(**vars(self))
            else:
                raise ValueError("Needs a callable factory.")

        result = type.__new__(metacls, name, bases, {})

        setattr(result, __init__.__name__, __init__)
        setattr(result, __getattr__.__name__, __getattr__)
        setattr(result, __getitem__.__name__, __getitem__)
        setattr(result, build.__name__, build)

        return result


class Builder(metaclass=_BuilderMeta):
    target = None
