# -------- Introspection (Reflection) in Python --------

# Here’s a comprehensive Python script I made that demonstrates various aspects of introspection (reflection) in Python,
# including inspecting types, accessing attributes, methods, and properties, invoking methods, working with
# custom attributes, dynamically creating objects, and more. This code is designed to cover a wide range
# of introspection capabilities at an expert level.


import inspect
import types


# Custom decorator (acts like an attribute in Python)
def custom_decorator(func):
    func.is_custom = True
    return func


# Custom class with various methods, properties, and attributes
class SampleClass:
    class_variable = "I am a class variable"

    def __init__(self, instance_variable):
        self.instance_variable = instance_variable

    @property
    def dynamic_property(self):
        return f"Dynamic property: {self.instance_variable}"

    @dynamic_property.setter
    def dynamic_property(self, value):
        self.instance_variable = value

    @staticmethod
    def static_method():
        return "This is a static method."

    @classmethod
    def class_method(cls):
        return f"Class method called from {cls.__name__}"

    @custom_decorator
    def decorated_method(self):
        return "This method is decorated."

    def regular_method(self, param1: int, param2: int) -> str:
        return f"Regular method called with params: {param1}, {param2}"


# Instantiate the class
sample_instance = SampleClass("Initial Value")

# Inspecting the instance type and class
print(f"Type of sample_instance: {type(sample_instance)}")
print(f"Class of sample_instance: {sample_instance.__class__.__name__}")

# Inspecting class attributes (but not specific instance attributes)
print("\nClass Attributes:")
for name, value in SampleClass.__dict__.items():
    if not name.startswith("__"):
        print(f"{name}: {value}")

# Inspecting instance attributes
print("\nInstance Attributes:")
for name, value in sample_instance.__dict__.items():
    print(f"{name}: {value}")

# Accessing and modifying an instance variable
print(f"\nOriginal instance_variable: {sample_instance.instance_variable}")
setattr(sample_instance, 'instance_variable', 'New Value')
print(f"Modified instance_variable: {getattr(sample_instance, 'instance_variable')}")  # "getattr" does the same as "sample_instance.instance_variable"

# Accessing and modifying a dynamic property
print(f"\nOriginal dynamic_property: {sample_instance.dynamic_property}")
sample_instance.dynamic_property = "Updated via property"
print(f"Updated dynamic_property: {sample_instance.dynamic_property}")

# Inspecting methods
print("\nMethods in SampleClass:")
for name, method in inspect.getmembers(SampleClass, predicate=inspect.isfunction):
    print(f"Method: {name}, Decorated: {'is_custom' in dir(method)}")

# Invoking methods dynamically
method_to_call = getattr(sample_instance, 'regular_method')
result = method_to_call('param1_value', 'param2_value')
print(f"\nResult of dynamically invoked regular_method: {result}")

# Accessing and invoking a decorated method
decorated_method = getattr(sample_instance, 'decorated_method')
if hasattr(decorated_method, 'is_custom'):
    print(f"\nDecorated Method: {decorated_method()}")

# Inspecting the source code of a method - see how the source code is actually written!!
print("\nSource code of 'regular_method':")
print(inspect.getsource(SampleClass.regular_method))

# Inspecting the signature of a method (the params it has, their type if specified and the return type if specified)
print("\nSignature of 'regular_method':")
signature = inspect.signature(SampleClass.regular_method)
print(signature)

# Inspecting the parameters of a method
print("\nParameters of 'regular_method':")
for param in signature.parameters.values():
    print(f"Name: {param.name}, Default: {param.default}, Annotation: {param.annotation}")

# Checking if an object is an instance of a particular class
is_instance = isinstance(sample_instance, SampleClass)
print(f"\nIs sample_instance an instance of SampleClass? {is_instance}")

# Checking if a class is a subclass of another class
is_subclass = issubclass(SampleClass, object)
print(f"Is SampleClass a subclass of object? {is_subclass}")


# Dynamically adding a new method to the class
def dynamic_method(self):
    return "This is a dynamically added method."


SampleClass.dynamic_method = types.MethodType(dynamic_method, SampleClass)
print(f"\nDynamically added method output: {sample_instance.dynamic_method()}")

# Dynamically creating an instance of a class
dynamic_instance = type('DynamicClass', (SampleClass,), {'extra_attribute': 42})('Dynamic Instance Value')
print(f"\nDynamically created instance type: {type(dynamic_instance)}")
print(f"Extra attribute in dynamic_instance: {dynamic_instance.extra_attribute}")
print(f"Instance variable in dynamic_instance: {dynamic_instance.instance_variable}")

# Checking if an object is callable
# Note: The callable() function in Python is used to check if an object appears to be callable, meaning that it can
# be called as a function. This function returns True if the object appears callable, and False otherwise.
print(f"\nIs sample_instance.regular_method callable? {callable(sample_instance.regular_method)}")

# Listing all callable attributes of an instance
print("\nList of callable attributes in sample_instance:")
for name in dir(sample_instance):
    attr = getattr(sample_instance, name)
    if callable(attr):
        print(f"Callable: {name}")


# Using reflection to call a method with arbitrary arguments
def call_method_with_args(obj, method_name, *args, **kwargs):
    method = getattr(obj, method_name, None)
    if callable(method):
        return method(*args, **kwargs)
    raise AttributeError(f"{method_name} is not callable on {obj}")


result = call_method_with_args(sample_instance, 'regular_method', 'arg1', 'arg2')
print(f"\nResult from call_method_with_args: {result}")


# Handling missing attributes with __getattr__
class FallbackClass:
    def __getattr__(self, name):
        return f"Attribute '{name}' not found, returning fallback value."


fallback_instance = FallbackClass()
print(f"\nAccessing missing attribute: {fallback_instance.nonexistent_attribute}")


# Handling dynamic attribute assignment with __setattr__
class DynamicAttributeClass:
    def __setattr__(self, name, value):
        print(f"Setting attribute '{name}' to '{value}'")
        super().__setattr__(name, value)


dynamic_attr_instance = DynamicAttributeClass()
dynamic_attr_instance.new_attr = "Assigned via __setattr__"

# Inspecting and invoking a lambda function
lambda_func = lambda x: x * 2
print(f"\nLambda function inspection:")
print(f"Is lambda_func a function? {callable(lambda_func)}")
print(f"Lambda function result: {lambda_func(10)}")
