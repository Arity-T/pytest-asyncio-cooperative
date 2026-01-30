import asyncio
import functools
import time

from ..fixtures import fill_fixtures


async def hypothesis_test_wrapper(item):
    """
    Hypothesis is synchronous, let's run inside an executor to keep asynchronicity
    """

    # Do setup
    item.start_setup = time.time()
    fixture_values, teardowns = await fill_fixtures(item)
    item.stop_setup = time.time()

    default_loop = asyncio.get_running_loop()
    inner_test = item.function.hypothesis.inner_test

def async_to_sync(inner_test, *args, **kwargs):
    # FIXME: can we cache this loop across multiple runs?
    loop = asyncio.get_event_loop()  # Use current loop instead of creating a new one
    task = inner_test(*args, **kwargs)
    try:
        return loop.run_until_complete(task)
    finally:
        pass  # No need to close the loop as we're using the current one
            pass
    item.stop_teardown = time.time()
