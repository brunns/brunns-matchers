import builtins
import types
from typing import Generic, TypeVar, get_args, get_origin

from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from brunns.matchers.utils import append_matcher_description, describe_field_match, describe_field_mismatch

BUILTINS = {name for name in dir(builtins) if isinstance(getattr(builtins, name), (types.BuiltinFunctionType, type))}
T = TypeVar("T")


class AutoMatcherMeta(type):
    def __new__(cls, name, bases, namespace, **_kwargs):  # noqa: C901
        if name == "BaseAutoMatcher":
            return super().__new__(cls, name, bases, namespace)

        domain_class = namespace.get("__domain_class__")

        if domain_class is None:
            orig_bases = namespace.get("__orig_bases__", [])
            for orig in orig_bases:  # pragma: no cover
                origin = get_origin(orig)
                args = get_args(orig)
                if origin is BaseAutoMatcher and args:
                    inferred_type = args[0]
                    if hasattr(inferred_type, "__annotations__"):
                        domain_class = inferred_type
                        namespace["__domain_class__"] = domain_class
                        break

        if domain_class is None or not hasattr(domain_class, "__annotations__"):
            msg = f"{name} must define or infer __domain_class__ with annotations"
            raise TypeError(msg)

        for field_name in domain_class.__annotations__:
            attr_name = f"{field_name}_" if field_name in BUILTINS else field_name
            namespace[attr_name] = anything()

        return super().__new__(cls, name, bases, namespace)


class BaseAutoMatcher(BaseMatcher, Generic[T], metaclass=AutoMatcherMeta):
    """Create matchers for classes. Use like so:

    ```python
    from dataclasses import dataclass
    from typing import Optional

    from hamcrest import assert_that, starts_with
    from hamcrest.core.matcher import Matcher
    from pydantic import BaseModel

    from brunns.matchers.meta import BaseAutoMatcher

    @dataclass
    class Status:
        id: int
        code: str
        reason: Optional[str] = None

    class StatusMatcher(BaseAutoMatcher[Status]): ...

    def is_status() -> Matcher[Status]:
        return StatusMatcher()

    status = Status(id=99, code="ACTIVE")

    def is_status() -> Matcher[Status]: return StatusMatcher()

    actual = Status(status_code="ACTIVE", count=99)
    assert_that(actual, is_status().with_code(starts_with("ACT")).and_reason(None))
    assert_that(actual, is_status().with_id(42))  # Will fail
    ```

    Works only for classes with `__annotations__`; typically manually annotated classes, dataclasses.dataclass and
    pydantic.BaseModel instances.
    """

    __domain_class__ = None  # Will be inferred when subclassed generically

    def describe_to(self, description: Description) -> None:
        description.append_text(f"{self.__domain_class__.__name__} with")  # type: ignore[attr-defined]
        for field_name in self.__domain_class__.__annotations__:
            attr_name = f"{field_name}_" if field_name in BUILTINS else field_name
            append_matcher_description(getattr(self, attr_name), field_name, description)

    def _matches(self, item: T) -> bool:
        return all(
            getattr(self, f"{field}_" if field in BUILTINS else field).matches(getattr(item, field))
            for field in self.__domain_class__.__annotations__
        )

    def describe_mismatch(self, item: T, mismatch_description: Description) -> None:
        mismatch_description.append_text(f"was {self.__domain_class__.__name__} with")  # type: ignore[attr-defined]
        for field_name in self.__domain_class__.__annotations__:
            matcher = getattr(self, f"{field_name}_" if field_name in BUILTINS else field_name)
            value = getattr(item, field_name)
            describe_field_mismatch(matcher, field_name, value, mismatch_description)

    def describe_match(self, item: T, match_description: Description) -> None:
        match_description.append_text(f"was {self.__domain_class__.__name__} with")  # type: ignore[attr-defined]
        for field_name in self.__domain_class__.__annotations__:
            matcher = getattr(self, f"{field_name}_" if field_name in BUILTINS else field_name)
            value = getattr(item, field_name)
            describe_field_match(matcher, field_name, value, match_description)

    def __getattr__(self, name: str):
        if name.startswith(("with_", "and_")):
            base = name.removeprefix("with_").removeprefix("and_")
            attr = f"{base}_" if base in BUILTINS else base
            if hasattr(self, attr):

                def setter(value):
                    setattr(self, attr, wrap_matcher(value))
                    return self

                return setter
        msg = f"{type(self).__name__} object has no attribute {name}"
        raise AttributeError(msg)

    def __dir__(self):
        dynamic_methods = []
        for field_name in self.__domain_class__.__annotations__:
            base = field_name.rstrip("_") if field_name in BUILTINS else field_name
            dynamic_methods.extend([f"with_{base}", f"and_{base}"])
        return list(super().__dir__()) + dynamic_methods
