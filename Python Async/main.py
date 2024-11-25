# async_cheatsheet_extended.py

# ================================
# Asynchronous Programming in Python
# ================================

# Python's asynchronous programming is centered around the `asyncio` library,
# which provides a foundation for writing single-threaded concurrent code using coroutines,
# event loops, and futures.

import asyncio
import random
import time

# ----------------
# 1. Coroutines
# ----------------
# A coroutine is a special type of function that can be paused and resumed,
# allowing other coroutines to run in the meantime.

# Basic Coroutine
async def simple_coroutine():
    print("Coroutine started")
    await asyncio.sleep(1)
    print("Coroutine ended")

# To run the coroutine, you need an event loop:
async def run_simple_coroutine():
    await simple_coroutine()

# Running the coroutine directly
# asyncio.run(run_simple_coroutine())

# Explanation:
# Coroutines are defined using the `async def` syntax. The `await` keyword is used to pause
# the coroutine's execution until the awaited coroutine (in this case, `asyncio.sleep(1)`) completes.

# ----------------
# 2. Awaiting Coroutines
# ----------------
# The `await` keyword is used to pause the execution of the coroutine until the awaited coroutine finishes.

async def another_coroutine():
    print("Another coroutine started")
    await asyncio.sleep(2)
    print("Another coroutine ended")

async def combined_coroutines():
    print("Starting combined coroutines")
    await simple_coroutine()
    await another_coroutine()
    print("All coroutines have finished")

# asyncio.run(combined_coroutines())

# Explanation:
# You can use `await` to pause a coroutine while another coroutine runs.
# This allows you to chain coroutines together, ensuring they run sequentially.

# ----------------
# 3. Running Coroutines Concurrently
# ----------------
# To run multiple coroutines concurrently, use `asyncio.gather` or `asyncio.create_task`.

async def task_1():
    print("Task 1 running")
    await asyncio.sleep(2)
    print("Task 1 done")

async def task_2():
    print("Task 2 running")
    await asyncio.sleep(3)
    print("Task 2 done")

async def run_concurrent_tasks():
    print("Running tasks concurrently")
    await asyncio.gather(task_1(), task_2())
    print("Both tasks have completed")

# asyncio.run(run_concurrent_tasks())

# Explanation:
# `asyncio.gather` runs multiple coroutines concurrently and waits for all of them to finish.
# The tasks run concurrently, not in parallel, because Python's `asyncio` is single-threaded.

# ----------------
# 4. Creating and Running Tasks
# ----------------
# Tasks wrap coroutines and allow them to be run concurrently.

async def task_with_return():
    print("Task with return value started")
    await asyncio.sleep(1)
    print("Task with return value ended")
    return "Task Result"

async def run_tasks_with_return():
    task = asyncio.create_task(task_with_return())
    result = await task
    print(f"Task returned: {result}")

# asyncio.run(run_tasks_with_return())

# Explanation:
# `asyncio.create_task` is used to schedule the execution of a coroutine. It returns an `asyncio.Task` object,
# which can be awaited to get the result of the coroutine.

# ----------------
# 5. Managing Task Lifetimes and Cancellation
# ----------------
# Tasks can be cancelled using `task.cancel()`.

async def long_running_task():
    print("Long running task started")
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("Task was cancelled")
        return
    print("Long running task ended")

async def run_and_cancel_task():
    task = asyncio.create_task(long_running_task())
    await asyncio.sleep(2)
    task.cancel()
    try:
        await task  # Ensures the task's cancellation is processed
    except asyncio.CancelledError:
        print("Handled task cancellation")

# asyncio.run(run_and_cancel_task())

# Explanation:
# Tasks can be cancelled with `task.cancel()`, which raises an `asyncio.CancelledError` inside the coroutine.
# This error can be caught and handled to clean up resources or take other actions.

# ----------------
# 6. Using `asyncio.sleep` and `asyncio.wait`
# ----------------
# `asyncio.sleep` is a coroutine that delays execution. `asyncio.wait` can be used to wait for multiple tasks.

async def delayed_task(delay):
    await asyncio.sleep(delay)
    return f"Completed after {delay} seconds"

async def run_delayed_tasks():
    tasks = [asyncio.create_task(delayed_task(i)) for i in range(1, 4)]
    done, pending = await asyncio.wait(tasks)
    for task in done:
        print(task.result())

# asyncio.run(run_delayed_tasks())

# Explanation:
# `asyncio.wait` waits for multiple tasks to complete. It returns two sets: `done` and `pending`,
# which contain the tasks that have finished and those that are still running, respectively.

# ----------------
# 7. Timeout Management
# ----------------
# `asyncio.wait_for` can be used to enforce timeouts on coroutines.

async def task_with_timeout():
    try:
        await asyncio.wait_for(delayed_task(5), timeout=2)
    except asyncio.TimeoutError:
        print("Task timed out")

# asyncio.run(task_with_timeout())

# Explanation:
# `asyncio.wait_for` waits for a coroutine to complete with a specified timeout.
# If the timeout expires before the coroutine finishes, a `TimeoutError` is raised.

# ----------------
# 8. Using `asyncio.Lock` and `asyncio.Semaphore`
# ----------------
# `asyncio.Lock` is used to prevent concurrent access to a shared resource.
# `asyncio.Semaphore` controls access to a resource with a limited number of slots.

# Example with asyncio.Lock
lock = asyncio.Lock()

async def task_with_lock(task_num):
    async with lock:
        print(f"Task {task_num} acquired the lock")
        await asyncio.sleep(2)
        print(f"Task {task_num} released the lock")

async def run_tasks_with_lock():
    await asyncio.gather(task_with_lock(1), task_with_lock(2))

# asyncio.run(run_tasks_with_lock())

# Example with asyncio.Semaphore
semaphore = asyncio.Semaphore(2)

async def task_with_semaphore(task_num):
    async with semaphore:
        print(f"Task {task_num} acquired the semaphore")
        await asyncio.sleep(2)
        print(f"Task {task_num} released the semaphore")

async def run_tasks_with_semaphore():
    await asyncio.gather(
        task_with_semaphore(1),
        task_with_semaphore(2),
        task_with_semaphore(3)
    )

# asyncio.run(run_tasks_with_semaphore())

# Explanation:
# `asyncio.Lock` ensures that only one coroutine can access a shared resource at a time.
# `asyncio.Semaphore` allows a limited number of coroutines to access a resource concurrently.

# ----------------
# 9. Synchronization Primitives
# ----------------
# `asyncio.Event`, `asyncio.Condition`, and `asyncio.Queue` can be used for advanced synchronization.

# asyncio.Event
event = asyncio.Event()

async def waiter():
    print("Waiting for event")
    await event.wait()
    print("Event triggered")

async def trigger():
    print("Triggering event")
    await asyncio.sleep(3)
    event.set()

async def run_event_demo():
    await asyncio.gather(waiter(), trigger())

# asyncio.run(run_event_demo())

# Explanation:
# `asyncio.Event` is a synchronization primitive that can be used to signal between coroutines.
# One coroutine can wait for an event, while another can trigger it using `event.set()`.

# asyncio.Condition
condition = asyncio.Condition()

async def producer():
    async with condition:
        print("Producing")
        await asyncio.sleep(2)
        condition.notify()

async def consumer():
    async with condition:
        print("Waiting for production")
        await condition.wait()
        print("Consumed")

async def run_condition_demo():
    await asyncio.gather(producer(), consumer())

# asyncio.run(run_condition_demo())

# Explanation:
# `asyncio.Condition` is used to synchronize access to a shared resource.
# Coroutines can wait on a condition and be notified when a certain state is reached.

# asyncio.Queue
queue = asyncio.Queue()

async def queue_producer():
    for i in range(5):
        await queue.put(i)
        print(f"Produced {i}")
        await asyncio.sleep(1)

async def queue_consumer():
    while True:
        item = await queue.get()
        print(f"Consumed {item}")
        if item == 4:
            break

async def run_queue_demo():
    await asyncio.gather(queue_producer(), queue_consumer())

# asyncio.run(run_queue_demo())

# Explanation:
# `asyncio.Queue` is an asynchronous queue that supports multiple producers and consumers.
# It is a thread-safe way to exchange items between coroutines.

# ----------------
# 10. Threading and Asyncio
# ----------------
# Sometimes you need to run blocking code in a separate thread to keep the event loop responsive.

def blocking_io():
    print("Starting blocking IO")
    time.sleep(3)
    print("Blocking IO finished")

async def run_blocking_in_thread():
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, blocking_io)
    print("Returned to event loop")

# asyncio.run(run_blocking_in_thread())

# Explanation:
# `loop.run_in_executor` runs a blocking function in a separate thread, preventing it from blocking the event loop.
# This is useful when you need to perform CPU-bound tasks or interact with blocking I/O.

# ----------------
# 11. Subprocesses with Asyncio
# ----------------
# `asyncio.create_subprocess_exec` and `asyncio.create_subprocess_shell` are used to create subprocesses.

async def run_subprocess():
    proc = await asyncio.create_subprocess_shell(
        "echo 'Hello World'",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()
    print(f"[stdout]: {stdout.decode()}")
    print(f"[stderr]: {stderr.decode()}")

# asyncio.run(run_subprocess())

# Explanation:
# `asyncio.create_subprocess_exec` and `asyncio.create_subprocess_shell` allow you to run subprocesses
# asynchronously. You can interact with the process's stdin, stdout, and stderr streams in a non-blocking manner.

# ----------------
# 12. Async Context Managers
# ----------------
# Async context managers are used with `async with`.

class AsyncContextManager:
    async def __aenter__(self):
        print("Entering context")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("Exiting context")

async def use_async_context_manager():
    async with AsyncContextManager() as acm:
        print("Using context manager")

# asyncio.run(use_async_context_manager())

# Explanation:
# Async context managers are defined using `__aenter__` and `__aexit__` methods.
# They are useful for managing resources that need to be acquired and released asynchronously.

# ----------------
# 13. Async Iterators and Generators
# ----------------
# Async iterators and generators are used with `async for`.

class AsyncIterable:
    def __init__(self):
        self.count = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.count >= 3:
            raise StopAsyncIteration
        self.count += 1
        await asyncio.sleep(1)
        return self.count

async def use_async_iterator():
    async for i in AsyncIterable():
        print(i)

# asyncio.run(use_async_iterator())

# Explanation:
# Async iterators implement `__aiter__` and `__anext__` methods.
# They allow you to iterate over asynchronous sequences using `async for`.

# Async Generators
async def async_generator():
    for i in range(3):
        await asyncio.sleep(1)
        yield i

async def use_async_generator():
    async for i in async_generator():
        print(i)

# asyncio.run(use_async_generator())

# Explanation:
# Async generators are defined using `async def` and can yield values asynchronously using `yield`.
# They are useful when you need to generate values over time, possibly interleaved with other asynchronous tasks.

# ----------------
# 14. Asyncio Streams
# ----------------
# `asyncio` provides APIs to handle network streams (TCP, UDP).

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    print(f"Received: {message}")
    writer.write(data)
    await writer.drain()
    print("Echoed back")
    writer.close()

async def run_server():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()

# asyncio.run(run_server())

async def run_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    writer.write(b"Hello Server")
    data = await reader.read(100)
    print(f"Received: {data.decode()}")
    writer.close()

# asyncio.run(run_client())

# Explanation:
# `asyncio.Streams` provide an interface to manage network connections asynchronously.
# You can create servers using `asyncio.start_server` and clients with `asyncio.open_connection`.
# The `StreamReader` and `StreamWriter` classes are used to read from and write to the connection.

# ----------------
# 15. Structured Concurrency with `asyncio.TaskGroup`
# ----------------
# `asyncio.TaskGroup` is introduced in Python 3.11 to manage task lifetimes more effectively.

async def task_group_example():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(task_1())
        tg.create_task(task_2())

# asyncio.run(task_group_example())

# Explanation:
# `asyncio.TaskGroup` is used to manage a group of tasks, ensuring they are all completed before
# the group is exited. This makes it easier to manage the lifetime of multiple tasks together.

# ================================
# Additional Advanced Topics
# ================================

# ----------------
# 16. Ensuring Thread Safety with `asyncio.Lock`
# ----------------

# Example with asyncio.Lock
lock = asyncio.Lock()

async def thread_safe_task(task_num):
    async with lock:
        print(f"Task {task_num} acquired the lock")
        await asyncio.sleep(2)
        print(f"Task {task_num} released the lock")

async def run_thread_safe_tasks():
    await asyncio.gather(thread_safe_task(1), thread_safe_task(2))

# asyncio.run(run_thread_safe_tasks())

# Explanation:
# `asyncio.Lock` ensures that only one coroutine can execute a block of code at a time.
# This is essential when you have shared resources that should not be accessed concurrently by multiple coroutines.

# ----------------
# 17. Using `asyncio.Event` to Implement Pub/Sub Model
# ----------------
# `asyncio.Event` can be used as a primitive for a Pub/Sub system where one or more consumers wait for an event to be set.

# Example: Pub/Sub Model using asyncio.Event
publisher_event = asyncio.Event()

async def publisher():
    print("Publisher waiting to publish...")
    await asyncio.sleep(3)
    print("Publisher published!")
    publisher_event.set()

async def subscriber(subscriber_id):
    print(f"Subscriber {subscriber_id} waiting for publication...")
    await publisher_event.wait()
    print(f"Subscriber {subscriber_id} received the publication!")

async def run_pub_sub_model():
    await asyncio.gather(publisher(), subscriber(1), subscriber(2))

# asyncio.run(run_pub_sub_model())

# Explanation:
# In this example, the publisher waits before setting the event (indicating that something has been published).
# The subscribers wait for this event before continuing, simulating a basic publish/subscribe model.

# ----------------
# 18. Exception Handling in Coroutines
# ----------------
# Exception handling in coroutines works just like in regular functions.
# However, unhandled exceptions in tasks will be propagated to the event loop.

async def task_with_exception():
    print("Task started")
    await asyncio.sleep(1)
    raise ValueError("Something went wrong!")
    print("Task completed")

async def run_task_with_exception_handling():
    try:
        await task_with_exception()
    except ValueError as e:
        print(f"Caught exception: {e}")

# asyncio.run(run_task_with_exception_handling())

# Explanation:
# Exceptions in coroutines can be caught and handled using `try/except`, just like in regular functions.
# If an exception is not caught, it will be propagated to the event loop, which may log it or handle it according to the event loop's configuration.

# ----------------
# 19. Understanding `asyncio.TimeoutError`
# ----------------
# `asyncio.TimeoutError` is raised when a coroutine does not complete within the specified timeout.

async def run_with_timeout():
    try:
        await asyncio.wait_for(delayed_task(5), timeout=2)
    except asyncio.TimeoutError:
        print("Operation timed out")

# asyncio.run(run_with_timeout())

# Explanation:
# `asyncio.TimeoutError` is a specific exception that is raised when a coroutine exceeds the time limit specified by `asyncio.wait_for`.

# ----------------
# 20. Performance Considerations
# ----------------
# Asyncio is best for IO-bound tasks and is not ideal for CPU-bound tasks. Consider using `concurrent.futures` for CPU-bound work.

# Example: CPU-bound task in a separate thread using concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def cpu_bound_task():
    print("Starting CPU-bound task")
    time.sleep(2)  # Simulate a heavy computation
    print("CPU-bound task finished")

async def run_cpu_bound_task():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, cpu_bound_task)
    print("Returned to event loop")

# asyncio.run(run_cpu_bound_task())

# Explanation:
# For CPU-bound tasks, it's often better to use threads or processes to avoid blocking the event loop.
# The `concurrent.futures.ThreadPoolExecutor` is a good choice for running CPU-bound tasks in separate threads.

# The examples provided cover most of the common and advanced scenarios you might encounter when working with asyncio.
# To fully understand and master async programming, hands-on practice and experimentation with these concepts are key.

# ================================
# End of Cheat Sheet
# ================================

