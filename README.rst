.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Project Directory Structure
==========================

```
.
├── LICENSE
├── README.rst
├── pyproject.toml
├── requirements.txt
├── example
│   ├── flakey.py
│   ├── hypothesis_test.py
│   ├── mixed.py
│   ├── module_fixture.py
│   └── skipped.py
├── pytest_asyncio_cooperative
│   ├── __init__.py
│   ├── assertion.py
│   ├── fixtures.py
│   └── plugin.py
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_autouse.py
│   ├── test_bugs.py
│   ├── test_class_based.py
│   ├── test_fail.py
│   ├── test_fixed.py
│   ├── test_fixture.py
│   ├── test_fixture_ducktyping.py
│   ├── test_fixture_object_passing.py
│   ├── test_fixture_ordering.py
│   ├── test_fixture_session.py
│   ├── test_junitxml.py
│   ├── test_known_issues.py
│   ├── test_lock.py
│   ├── test_max_asyncio_tasks.py
│   └── test_parameterize.py
```

Use asyncio (cooperative multitasking) to run your I/O bound test suite efficiently and quickly.

.. code-block:: python
   :class: ignore
   
   import asyncio

   import pytest
   
   @pytest.mark.asyncio_cooperative
   async def test_a():
       await asyncio.sleep(2)
   
   
   @pytest.mark.asyncio_cooperative
   async def test_b():
       await asyncio.sleep(2)


.. code-block:: bash
   :class: ignore

   ========== 2 passed in 2.05 seconds ========== 


Quickstart
----------
.. code-block:: bash
   :class: ignore

   pip install pytest-asyncio-cooperative


Compatibility
-------------
pytest-asyncio is NOT compatible with this plugin. Please uninstall pytest-asyncio or pass this flag to pytest `-p no:asyncio`

Fixtures
--------
It's recommended that async tests use async fixtures.

.. code-block:: bash
   :class: ignore

   import asyncio
   import pytest


   @pytest.fixture
   async def my_fixture():
       await asyncio.sleep(2)
       yield 