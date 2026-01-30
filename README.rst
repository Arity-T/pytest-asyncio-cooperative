.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Используйте asyncio (кооперативная многозадачность), чтобы запускать свой тестовый набор, связанный с вводом-выводом, эффективно и быстро.

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
pytest-asyncio НЕ совместим с этим плагином. Пожалуйста, удалите pytest-asyncio или передайте этот флаг pytest `-p no:asyncio`

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

- Уменьшить общее время выполнения тестов, связанных с вводом-выводом, через кооперативную многозадачность

- Снизить использование системных ресурсов через кооперативную многозадачность


Плюсы
----

- Тестовый набор, связанный с вводом-выводом, будет выполняться быстрее (например, отдельные тесты будут занимать столько же времени. Общее время выполнения всего тестового набора будет быстрее)

- Тестовый набор, связанный с вводом-выводом, будет использовать меньше системных ресурсов (например, используется только один поток)

Минусы
----

- Порядок тестов не гарантируется (например, некоторые блокирующие операции могут занять больше времени и повлиять на порядок результатов тестов)

- Тесты ДОЛЖНЫ быть изолированными друг от друга (например, НЕТ общих ресурсов, НЕТ `mock.patch`). Однако, имейте в виду, что замки могут использоваться для обеспечения изоляции.

- Нет параллелизма, тесты, зависящие от ЦП, НЕ получат выгоду от производительности


Моки и Общие Ресурсы
------------------------

При использовании моков и общих ресурсов кооперативная многозадачность означает, что тесты могут иметь гоночные условия.

В этом случае вы можете использовать замки:

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

В приведенном выше примере важно поместить фикстуру `lock` на крайнюю левую сторону, чтобы обеспечить взаимное исключение.

Тайм-ауты
--------

Тесты автоматически отменяются после тайм-аута в 600 секунд. Вы можете изменить это с помощью опции `--asyncio-task-timeout` или добавив запись `asyncio_task_timeout` в ваш файл `pytest.ini`.

Максимальное количество асинхронных задач
--------------------------

Иногда вы хотите ограничить количество одновременно выполняемых задач. Вы можете установить максимум с помощью опции `--max-asyncio-tasks`, добавив запись `max_asyncio_tasks` в ваш файл `pytest.ini`.