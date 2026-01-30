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
        """Convert an asynchronous function into a synchronous one."
        # FIXME: can we cache this loop across multiple runs?
        loop = asyncio.new_event_loop()
        task = inner_test(*args, **kwargs)
        try:
            loop.run_until_complete(task)
        finally:
            loop.close()
            pass
    item.stop_teardown = time.time()
