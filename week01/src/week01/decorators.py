"""Day 3 - decorators: middleware around a single function."""

import functools
import time
from collections.abc import Callable
from typing import Any

def timed(func: Callable[..., Any]) -> Callable[...,Any]:
    """Log how long func takes, like a Stopwatch in an action filter."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            print(f"[timed] {func.__name__} took {elapsed_ms:.1f} ms")

    return wrapper

def retry(times: int = 3, delay: float = 0.1, exceptions: tuple[type[Exception], ...] = (Exception,)):
    """Decorator WITH arguments: retry(...) returns the real decorator. Think Polly."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == times:
                        raise
                    print(f"[retry] {func.__name__} failed ({exc}); attempt {attempt + 1}/{times}")
                    time.sleep(delay)
            raise RuntimeError("unreachable")

        return wrapper

    return decorator

def count_calls(func : Callable[...,Any])  ->Callable[...,Any] :
       """Keeps state on the wrapper itself: functions are objects, so they can have attributes."""

       @functools.wraps(func)
       def wrapper(*args: Any, **kwargs: Any) -> Any:
           wrapper.calls +=1
           return func(*args,**kwargs)
       wrapper.calls=0
       return wrapper

TOOLS:dict[str, Callable[..., Any]] ={}

def tool(func: Callable[...,Any]) -> Callable[... ,Any] :
    """Register func by name and return it unchanged (no wrapper needed)."""
    TOOLS[func.__name__] = func
    return func

@tool
@timed
def slow_square(x: int) -> int :
     """Square a number, slowly."""
     time.sleep(0.05)
     return x*x

@functools.cache
def fib(n:int) -> int:
    return n if n < 2 else fib(n-1)+fib(n-2) 

_flaky_state={"calls":0}

@retry(times=3, delay=0.01, exceptions=(ConnectionError,))
def flaky_service() ->str :
    _flaky_state["calls"] += 1
    if _flaky_state["calls"] < 3 :
        raise ConnectionError("Service unavailable")
    return "ok"

if __name__ == "__main__":
    print(slow_square(12))
    print(slow_square.__name__, "-", slow_square.__doc__)  # preserved by functools.wraps
    print(fib(80))  # instant thanks to @cache
    print(flaky_service())
    print("registered tools:", list(TOOLS))