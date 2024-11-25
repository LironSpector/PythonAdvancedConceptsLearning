# ---- Python Generators - All examples and scenarios where generators might be used ----

# 1. Basic Generator Examples
# Example 1: Simple generator
def count_up_to(max):
    count = 1
    while count <= max:
        yield count
        count += 1


generator = count_up_to(3)
print(generator.__next__())
print(generator.__next__())
print(generator.__next__())
try:
    print(generator.__next__())
except Exception as e:
    print("All generator items were called already", e)


# Example 2: Generator with multiple yield statements
def generator():
    yield 'First'
    yield 'Second'
    yield 'Third'


another_gen = generator()
print(next(another_gen))  # First
print(another_gen.__next__())  # Second (next() and .__next__() does the same thing)


# Example 3: Using yield in a loop
def even_numbers(max):
    for n in range(max):
        if n % 2 == 0:
            yield n


even_nums = even_numbers(10)
for even in even_nums:
    print(even)


# Example 4: A generator function that yields values one at a time.
def simple_generator():
    yield 1
    yield 2
    yield 3


gen = simple_generator()
for value in gen:
    print(value)


# 2. Generator with Loop
# A generator that yields a sequence of values using a loop.
def countdown(n):
    while n > 0:
        yield n
        n -= 1


gen = countdown(5)
for value in gen:
    print(value)


# 3. Using send() to Send Values to a Generator
# You can interact with the generator during its execution using the send() method.
def coroutine():
    while True:
        value = yield
        print(f'Received: {value}')


gen = coroutine()
next(gen)  # Prime the generator - which means it advances the generator to the first yield statement, allowing it to
# start receiving values with the send() method.
gen.send(10)
gen.send(20)


# 4. Closing a Generator
# The close() method allows you to close a generator, triggering a GeneratorExit exception.
def controlled_generator():
    try:
        while True:
            value = yield
            print(f'Processing {value}')
    except GeneratorExit:
        print('Generator closed.')


gen = controlled_generator()
next(gen)  # Prime the generator
gen.send(10)
gen.send(20)
gen.close()  # Close the generator and clean up any resources it might be using
# gen.send(30)  # This will trigger an error


# 5. Throwing an Exception in a Generator
# The throw() method forces an exception at a particular yield statement inside the generator.
def exception_generator():
    try:
        yield 'Normal execution'
        yield 'Normal execution 2'
    except ValueError:
        yield 'Exception caught'


gen = exception_generator()
print(next(gen))
print(gen.throw(ValueError))
# print(next(gen))  # This will trigger an error


# 6. Generator with return Statement
# A generator can use the return statement to signal the end of iteration, raising a StopIteration exception.
def generator_with_return():
    yield 'Start'
    return 'End'


gen = generator_with_return()
try:
    print(next(gen))
    print(next(gen))
except StopIteration as e:
    print(f'Generator returned: {e.value}')


# 7. Delegating Generators with yield from
# You can delegate part of the generator’s operation to another generator using the yield from expression.
def sub_generator():
    yield 1
    yield 2


def main_generator():
    yield 'A'
    yield from sub_generator()
    yield 'B'


for value in main_generator():
    print(value)


# 8. Infinite Generators
# Generators can produce an infinite sequence of values, useful for streams of data.
def infinite_sequence(start=0):
    while True:
        yield start
        start += 1


gen = infinite_sequence()
for i in range(5):
    print(next(gen))


# 9. Combining Generators
# Multiple generators can be combined to create a more complex sequence.
def generator1():
    yield 'A'
    yield 'B'


def generator2():
    yield '1'
    yield '2'


def combined_generator():
    yield from generator1()
    yield from generator2()


for value in combined_generator():
    print(value)


# 10. Generator Expression
# A compact way to create a generator, similar to a list comprehension but returns a generator object.
gen_exp = (x**2 for x in range(5))
print(type(gen_exp))
for value in gen_exp:
    print(value)


# 11. Using itertools with Generators
# The itertools module provides several tools that work seamlessly with generators.
import itertools


def limited_count():
    for i in itertools.islice(itertools.count(10, 2), 5):
        yield i


gen = limited_count()
for value in gen:
    print(value)


# 12. Stopping a Generator with a Condition
# A generator can be stopped when a certain condition is met.
def stop_condition():
    for i in range(10):
        if i == 5:
            break
        yield i


gen = stop_condition()
for value in gen:
    print(value)
