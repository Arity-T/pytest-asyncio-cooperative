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
    def async_to_sync(*args, keep_loop_open=False, **kwargs):
        # Improved implementation for caching the loop across multiple calls
        if not hasattr(async_to_sync, '_loop'):
            async_to_sync._loop = asyncio.new_event_loop()  # Cache the new event loop
        loop = async_to_sync._loop
        task = inner_test(*args, **kwargs)
        try:
            loop.run_until_complete(task)
        finally:
            if not keep_loop_open:
                loop.close()  # Close the loop if not reused

    item.function.hypothesis.inner_test = async_to_sync
    wrapped_func_with_fixtures = functools.partial(item.function, *fixture_values)
    await default_loop.run_in_executor(None, wrapped_func_with_fixtures)

    # Do teardowns
    item.start_teardown = time.time()
    for teardown in teardowns:
        try:
            await teardown.__anext__()
        except StopAsyncIteration:
            pass
    item.stop_teardown = time.time()