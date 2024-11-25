# With this method, to solve the diamond problem, instead of calling in D, B and C with super().__init__,
class A:
    def __init__(self, name):
        self.__name = name  # Private attribute
        print(f"Initializing A: {self.__name}")

    # Getter for name
    @property
    def name(self):
        return self.__name

    # Setter for name
    @name.setter
    def name(self, name):
        self.__name = name

    def do_something(self):
        print(f"A's implementation of do_something for {self.__name}")

    def __str__(self):
        return f"Class A: {self.__name}"


class B(A):
    def __init__(self, name, age):
        # Call A's __init__ to ensure proper initialization
        A.__init__(self, name)
        self.__age = age  # Private attribute
        print(f"Initializing B: {self.name}, Age: {self.__age}")

    # Getter for age
    @property
    def age(self):
        return self.__age

    # Setter for age
    @age.setter
    def age(self, age):
        self.__age = age

    def do_something(self):
        print(f"B's implementation of do_something for {self.name}")
        # Use super() to ensure that A's implementation is still called
        super().do_something()

    def __str__(self):
        return f"Class B: {self.name}, Age: {self.__age}"


class C(A):
    def __init__(self, name, gender):
        # Call A's __init__ to ensure proper initialization
        A.__init__(self, name)
        self.__gender = gender  # Private attribute
        print(f"Initializing C: {self.name}, Gender: {self.__gender}")

    # Getter for gender
    @property
    def gender(self):
        return self.__gender

    # Setter for gender
    @gender.setter
    def gender(self, gender):
        self.__gender = gender

    def do_something(self):
        print(f"C's implementation of do_something for {self.name}")
        # Use super() to ensure that A's implementation is still called
        super().do_something()

    def __str__(self):
        return f"Class C: {self.name}, Gender: {self.__gender}"


class D(B, C):
    def __init__(self, name, age, gender, occupation):
        # Call both B and C's __init__ methods to initialize them properly
        B.__init__(self, name, age)
        C.__init__(self, name, gender)
        self.__occupation = occupation  # Private attribute
        print(f"Initializing D: {self.name}, Age: {self.age}, Gender: {self.gender}, Occupation: {self.__occupation}")

    # Getter for occupation
    @property
    def occupation(self):
        return self.__occupation

    # Setter for occupation
    @occupation.setter
    def occupation(self, occupation):
        self.__occupation = occupation

    def do_something(self):
        print(f"D's implementation of do_something for {self.name}")
        # Use super() to trigger the method resolution order
        super().do_something()

    def __str__(self):
        return f"Class D: {self.name}, Age: {self.age}, Gender: {self.gender}, Occupation: {self.__occupation}"


# Test the diamond problem structure and method resolution order

# Initialize an object of class D
person = D(name="John", age=30, gender="Male", occupation="Engineer")

# Test property getters
print("\nTesting Property Getters:")
print(f"Name: {person.name}")
print(f"Age: {person.age}")
print(f"Gender: {person.gender}")
print(f"Occupation: {person.occupation}")

# Change the attributes using property setters
person.name = "Jane"
person.age = 28
person.gender = "Female"
person.occupation = "Scientist"

# Print updated values
print("\nUpdated Values:")
print(f"Name: {person.name}")
print(f"Age: {person.age}")
print(f"Gender: {person.gender}")
print(f"Occupation: {person.occupation}")

# Call the do_something method, which triggers the diamond problem structure
person.do_something()

# Output the MRO (Method Resolution Order)
print("\nMethod Resolution Order (MRO):")
for cls in D.mro():
    print(cls)

# Output the string representation (__str__)
print("\nString Representation of Object D:")
print(person)

