from typing import Any, Callable
import pytest
from pycallgrind import start_instrumentation, stop_instrumentation, zero_stats, dump_stats_at


@pytest.fixture
def callbench(request: pytest.FixtureRequest):
    def run(func: Callable[..., Any], *args: Any):
        zero_stats()
        start_instrumentation()
        func(*args)
        stop_instrumentation()
        dump_stats_at(f'{request.node.nodeid}'.encode('ascii'))

    return run


@pytest.fixture
def benchmark(callbench):
    """
    Compatibility with pytest-benchmark
    """
    return callbench
