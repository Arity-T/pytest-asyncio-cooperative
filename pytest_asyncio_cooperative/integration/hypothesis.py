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

    def async_to_sync(*args, **kwargs):
        # Improved implementation for caching the loop across multiple calls
        if not hasattr(async_to_sync, '_loop'):  # Check if the loop is already cached
            async_to_sync._loop = asyncio.new_event_loop()  # Cache the new event loop
        loop = async_to_sync._loop
        task = inner_test(*args, **kwargs)
        try:
            loop.run_until_complete(task)
        finally:
            # Loop closing can be handled elsewhere or removed depending on use case
            pass  # Removed loop.close() to retain cached loop during multiple runs

        except StopAsyncIteration:
            pass
    item.stop_teardown = time.time()
