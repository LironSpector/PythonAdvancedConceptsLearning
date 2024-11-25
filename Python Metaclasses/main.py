# ---- Metaclasses in Python ----

# -- Example 1 - basic example: --
class MyMeta(type):
    def __new__(metacls, name, bases, dct):
        print(f"Creating class {name} with metaclass {metacls}")
        return super().__new__(metacls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        print(f"Initializing class {name}")
        super().__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        print(f"Creating instance of {cls.__name__}")
        return super().__call__(*args, **kwargs)


# Using the custom metaclass
class MyClass(metaclass=MyMeta):
    def __init__(self, x):
        self.x = x


# Creating an instance
obj = MyClass(10)




# -- Example 2 - Here is an example that demonstrates a metaclass enforcing a class attribute: --
class AttributeEnforcer(type):
    def __init__(cls, name, bases, dct):
        if 'required_attr' not in dct:
            raise AttributeError(f"{name} must have a 'required_attr' attribute")
        super().__init__(name, bases, dct)


class MyClassSecond(metaclass=AttributeEnforcer):
    required_attr = 42


# This will raise an AttributeError because 'required_attr' is missing in AnotherClass
# class AnotherClass(metaclass=AttributeEnforcer):
#     pass


# This will work because 'required_attr' is defined in MyClass
my_instance = MyClassSecond()

# This will raise an AttributeError because 'required_attr' is missing in AnotherClass
# another_instance = AnotherClass()




# -- Example 3 - Modifying Instance Creation: Singleton with Metaclasses --
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonClass(metaclass=SingletonMeta):
    def __init__(self):
        print("Creating a SingletonClass instance")


# All instances of SingletonClass will be the same
s1 = SingletonClass()
s2 = SingletonClass()

assert s1 is s2  # This will be True
print(s1 == s2)  # True
