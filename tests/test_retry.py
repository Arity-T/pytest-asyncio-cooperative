import sys

import pytest


@pytest.mark.skipif(sys.version_info < (3, 9), reason="Requires Python 3.9+")
def test_retry(testdir):
    # Use the pytest-retry plugin to retry the test
    # This test is handy because it tests "wrap_in_sync" logic

    testdir.makeconftest("""""")

    testdir.makepyfile(
        """
        import asyncio
        import pytest
        import uuid

        count = 0

        @pytest.mark.flaky
        @pytest.mark.asyncio_cooperative
        async def test_a():
            global count
            count += 1
@pytest.mark.flaky(2)
        @pytest.mark.asyncio_cooperative
    """
    )

    result = testdir.runpytest()

    result.assert_outcomes(
        errors=0, failed=0, passed=1, xfailed=0, xpassed=0, skipped=0
    )
