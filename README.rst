


Перевод Readme на русский язык
===========================

Весь текст в ридми переведен ниже:

Используйте asyncio (кооперативное многозадачность), чтобы эффективно и быстро управлять вашим набором тестов, зависящим от ввода/вывода.

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


Быстрый старт
----------
.. code-block:: bash
   :class: ignore

   pip install pytest-asyncio-cooperative


Совместимость
-------------
pytest-asyncio не совместим с этим плагином. Пожалуйста, удалите pytest-asyncio или передайте этот флаг в pytest `-p no:asyncio`


Фикстуры
--------
Рекомендуется, чтобы асинхронные тесты использовали асинхронные фикстуры.

.. code-block:: bash
   :class: ignore

   import asyncio
   import pytest


   @pytest.fixture
   async def my_fixture():
       await asyncio.sleep(2)
       yield "XXX"
       await asyncio.sleep(2)


   @pytest.mark.asyncio_cooperative
   async def test_a(my_fixture):
       await asyncio.sleep(2)
       assert my_fixture == "XXX"


Цели
-----

- Уменьшить общее время выполнения тестов, зависящих от ввода/вывода, с помощью кооперативной многозадачности

- Уменьшить использование системных ресурсов с помощью кооперативной многозадачности


Преимущества
----

- Тесты, зависящие от ввода/вывода, будут выполняться быстрее (т.е. отдельные тесты будут занимать столько же времени. Общее время выполнения всего набора тестов будет быстрее)

- Тесты, зависящие от ввода/вывода, будут использовать меньше системных ресурсов (т.е. используется только один поток)

Недостатки
----

- Порядок тестов не гарантируется (т.е. некоторые операции блокировки могут занять больше времени и повлиять на порядок результатов тестов)

- Тесты ДОЛЖНЫ быть изолированы друг от друга (т.е. НИКАКИХ общих ресурсов, НИКАКИХ `mock.patch`). Однако, обратите внимание, что блокировки могут быть использованы для обеспечения изоляции.

- Параллелизма НЕТ, тесты, зависящие от процессора, НЕ получат повышения производительности


Моки и общие ресурсы
------------------------

При использовании моков и общих ресурсов кооперативная многозадачность означает, что тесты могут иметь состояния гонки.

В этом случае вы можете использовать блокировки:

.. code-block:: bash
   :class: ignore

   import asyncio
   import pytest
   from pytest_asyncio_cooperative import Lock

   my_lock = Lock()

   @pytest.fixture(scope="function")
   async def lock():
       async with my_lock():
           yield

   @pytest.mark.asyncio_cooperative
   async def test_a(lock, mocker):
       await asyncio.sleep(2)
       mocker.patch("service.http.on_handler")
       access_shared_resource()
       assert my_fixture == "XXX"

   @pytest.mark.asyncio_cooperative
   async def test_b(lock, mocker):
       await asyncio.sleep(2)
       mocker.patch("service.http.on_handler")
       access_shared_resource()
       assert my_fixture == "XXX"

В приведенном выше примере важно разместить фикстуру `lock` на самой левой стороне, чтобы гарантировать взаимную эксклюзивность.

Тайм-ауты
--------

Тесты автоматически отменяются после тайм-аута в 600 секунд. Вы можете изменить это с помощью параметра `--asyncio-task-timeout` или добавив элемент `asyncio_task_timeout` в свой файл `pytest.ini`.

Максимальное количество асинхронных задач
--------------------------

Иногда вы хотите ограничить количество задач, работающих одновременно. Вы можете установить максимум с помощью параметра `--max-asyncio-tasks`, добавив элемент `max_asyncio_tasks` в свой файл `pytest.ini`.
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

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
       yield "XXX"
       await asyncio.sleep(2)


   @pytest.mark.asyncio_cooperative
   async def test_a(my_fixture):
       await asyncio.sleep(2)
       assert my_fixture == "XXX"


Goals
-----

- Reduce the total run time of I/O bound test suites via cooperative multitasking

- Reduce system resource usage via cooperative multitasking


Pros
----

- An I/O bound test suite will run faster (ie. individual tests will take just as long. The total runtime of the entire test suite will be faster)

- An I/O bound test suite will use less system resources (ie. only a single thread is used)

Cons
----

- Order of tests is not guaranteed (ie. some blocking operations might taken longer and affect the order of test results)

- Tests MUST be isolated from each other (ie. NO shared resources, NO `mock.patch`). However, note that locks can be used to ensure isolation.

- There is NO parallelism, CPU bound tests will NOT get a performance benefit


Mocks & Shared Resources
------------------------

When using mocks and shared resources cooperative multitasking means tests could have race conditions.

In this case you can use locks:

.. code-block:: bash
   :class: ignore

   import asyncio
   import pytest
   from pytest_asyncio_cooperative import Lock

   my_lock = Lock()

   @pytest.fixture(scope="function")
   async def lock():
       async with my_lock():
           yield

   @pytest.mark.asyncio_cooperative
   async def test_a(lock, mocker):
       await asyncio.sleep(2)
       mocker.patch("service.http.on_handler")
       access_shared_resource()
       assert my_fixture == "XXX"

   @pytest.mark.asyncio_cooperative
   async def test_b(lock, mocker):
       await asyncio.sleep(2)
       mocker.patch("service.http.on_handler")
       access_shared_resource()
       assert my_fixture == "XXX"

In the above example it's important to put the `lock` fixture on the far left-hand side to ensure mutual exclusivity.

Timeouts
--------

Tests are automatically cancelled after a timeout of 600s. You can change this with the `--asyncio-task-timeout` option or by adding an `asyncio_task_timeout` entry to your `pytest.ini` file.

Maximum Asynchronous Tasks
--------------------------

Sometimes you want to limit the number of tasks running concurrently. You can set a maximum with the `--max-asyncio-tasks` option by adding a `max_asyncio_tasks` entry to your `pytest.ini` file.
