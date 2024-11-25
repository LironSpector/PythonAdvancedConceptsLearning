# ---- Python Decorators ----

# Example 1:
def func(f):
    def wrapper(*args, **kwargs): # To match any number of parameters that may be passed, *args and **kwargs are used.
        print("Started")
        rv = f(*args, **kwargs)  # rv = return value
        print("Ended")
        return rv
    return wrapper

@func
def func2(x, y):
    print(x)
    return y

@func
def func3():
    print("I am func3")


output = func2(5, 6)
print(f"return value: {output}\n")

func3()



# -- Real World Examples: --
# Example 2 - Logging information about function calls:
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Function {func.__name__} called with arguments: {args} and {kwargs}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned: {result}")
        return result
    return wrapper


@log_decorator
def add(a, b):
    return a + b


result = add(10, 20)



# Example 3 - Access Control:
# Decorators can also be used to control access to a function. For example, checking if a user has the right permissions to execute a function.
def requires_permission(permission):
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if user.has_permission(permission):
                return func(user, *args, **kwargs)
            else:
                raise PermissionError(f"User does not have {permission} permission")
        return wrapper
    return decorator


class User:
    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions

    def has_permission(self, permission):
        return permission in self.permissions


@requires_permission('admin')
def delete_user(user, username):
    print(f"User {username} deleted by {user.name}")


admin_user = User('admin', ['admin'])
normal_user = User('normal', [])

delete_user(admin_user, 'test_user')  # This will succeed
# delete_user(normal_user, 'test_user') # This will raise PermissionError



# Example 4 - Memoization (Caching):
# A more advanced use of decorators is for memoization, where the decorator stores the results of expensive
# function calls and returns the cached result when the same inputs occur again.
def memoize(func):
    cache = {}
    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            result = func(*args)
            cache[args] = result
            return result
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


print(fibonacci(10))



# Example 5 - Chaining Multiple Decorators:
# You can also chain multiple decorators to a single function. When multiple decorators are applied to a function,
# they are applied in the order they are listed.
def bold(func):
    def wrapper():
        return f"<b>{func()}</b>"
    return wrapper


def italic(func):
    def wrapper():
        return f"<i>{func()}</i>"
    return wrapper


@bold
@italic
def greet():
    return "Hello"

print(greet())



# Example 6 - Class-based Decorators:
# You can also create decorators using classes. This can be useful if you need to maintain state or need more control.
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__}")
        return self.func(*args, **kwargs)


@CountCalls
def say_hello():
    print("Hello!")


@CountCalls
def say_bye():
    print("Bye!")


print("\nClass-based Decorators:")
say_hello()
say_hello()
say_bye()
say_bye()
say_hello()
say_hello()




# Other times where I might want to use decorators:
# When checking how much time it took for a function to run
# When validating the parameters passed to several functions (if the validation is more or less the same)
