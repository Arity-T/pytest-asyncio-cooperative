.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Используйте asyncio (кооперативная многозадачность), чтобы эффективно и быстро запускать наборы I/O-зависимых тестов.

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
------------
.. code-block:: bash
   :class: ignore

   pip install pytest-asyncio-cooperative


Совместимость
-------------
pytest-asyncio НЕ совместим с этим плагином. Пожалуйста, удалите pytest-asyncio или передайте в pytest флаг `-p no:asyncio`.

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
----

- Сократить общее время выполнения I/O-зависимых тестовых наборов за счет кооперативной многозадачности

- Снизить использование системных ресурсов за счет кооперативной многозадачности


Плюсы
-----

- I/O-зависимый набор тестов будет выполняться быстрее (т.е. отдельные тесты будут выполняться столько же. Общее время выполнения всего набора тестов будет меньше)

- I/O-зависимый набор тестов будет использовать меньше системных ресурсов (т.е. используется только один поток)

Минусы
------

- Порядок тестов не гарантируется (т.е. некоторые блокирующие операции могут выполняться дольше и влиять на порядок результатов тестов)

- Тесты ДОЛЖНЫ быть изолированы друг от друга (т.е. НЕТ общих ресурсов, НЕТ `mock.patch`). Однако обратите внимание, что блокировки можно использовать для обеспечения изоляции.

- Параллелизма НЕТ, CPU-зависимые тесты НЕ получат преимущества в производительности


Моки и общие ресурсы
--------------------

При использовании моков и общих ресурсов кооперативная многозадачность означает, что тесты могут иметь гонки.

В этом случае можно использовать блокировки:

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

В приведенном выше примере важно разместить фикстуру `lock` в самом левом положении, чтобы обеспечить взаимное исключение.

Таймауты
--------

Тесты автоматически отменяются после таймаута 600 секунд. Вы можете изменить это с помощью опции `--asyncio-task-timeout` или добавив параметр `asyncio_task_timeout` в файл `pytest.ini`.

Максимум асинхронных задач
--------------------------

Иногда нужно ограничить количество задач, выполняющихся одновременно. Вы можете установить максимум с помощью опции `--max-asyncio-tasks`, добавив параметр `max_asyncio_tasks` в файл `pytest.ini`.
