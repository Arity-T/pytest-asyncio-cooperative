.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

# Перевод Readme на русский язык

Используйте asyncio (сотрудничающее многозадачное выполнение), чтобы эффективно и быстро запустить свой тестовый набор, зависящий от ввода-вывода.

.. код-блок:: python
   :class: ignore
   
   import asyncio

   import pytest
   
   @pytest.mark.asyncio_cooperative
   async def test_a():
       await asyncio.sleep(2)
   
   
   @pytest.mark.asyncio_cooperative
   async def test_b():
       await asyncio.sleep(2)


.. код-блок:: bash
   :class: ignore

   ========== 2 пройдены за 2.05 секунд ========== 


Быстрый старт
----------
.. код-блок:: bash
   :class: ignore

   pip install pytest-asyncio-cooperative


Совместимость
-------------
pytest-asyncio несовместим с этим плагином. Пожалуйста, удалите pytest-asyncio или передайте этот флаг pytest `-p no:asyncio`


Фикстуры
--------
Рекомендуется, чтобы асинхронные тесты использовали асинхронные фикстуры.

.. код-блок:: bash
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

- Уменьшить общее время выполнения тестового набора, зависящего от ввода-вывода, за счет сотрудничества в многозадачности

- Снизить использование системных ресурсов за счет сотрудничества в многозадачности


Преимущества
----

- Тестовый набор, зависящий от ввода-вывода, будет работать быстрее (то есть, отдельные тесты займут столько же времени. Общее время выполнения всего тестового набора будет быстрее)

- Тестовый набор, зависящий от ввода-вывода, будет использовать меньше системных ресурсов (то есть используется только один поток)


Недостатки
----

- Порядок тестов не гарантирован (то есть, некоторые блокирующие операции могут занять больше времени и повлиять на порядок результатов тестов)

- Тесты ДОЛЖНЫ быть изолированы друг от друга (то есть НЕТ общих ресурсов, НЕТ `mock.patch`). Однако стоит отметить, что блокировки могут быть использованы для обеспечения изоляции.

- Нет параллелизма, тесты, зависящие от ЦП, НЕ получат преимущества в производительности


Моки и общие ресурсы
------------------------

При использовании моков и общих ресурсов, сотрудничающее многозадачное выполнение означает, что тесты могут иметь состояния гонки.

В этом случае вы можете использовать блокировки:

.. код-блок:: bash
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

В приведенном выше примере важно поместить фикстуру `lock` на крайний левый край, чтобы обеспечить взаимное исключение.


Тайм-ауты
--------

Тесты автоматически отменяются после тайм-аута в 600 секунд. Вы можете изменить это с помощью параметра `--asyncio-task-timeout` или добавив элемент `asyncio_task_timeout` в ваш файл `pytest.ini`.

Максимальное количество асинхронных задач
--------------------------

Иногда вы хотите ограничить количество задач, работающих одновременно. Вы можете установить максимум с помощью параметра `--max-asyncio-tasks`, добавив элемент `max_asyncio_tasks` в ваш файл `pytest.ini`.

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
