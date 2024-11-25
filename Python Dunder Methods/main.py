# ---- Good and Accurate Dunder/Magic Methods Implementation Example in Python ----
class Vector:
    def __init__(self, *components):
        """Initialize the Vector with its components."""
        self.components = components
        print(f"Vector{self.components} has been created.")

    def __new__(cls, *components):
        """Create and return a new instance of Vector."""
        return super(Vector, cls).__new__(cls)

    def __repr__(self):
        """Return the official string representation of the Vector."""
        return f"Vector{self.components}"

    def __str__(self):
        """Return the informal string representation of the Vector."""
        return f"Vector with components: {self.components}"

    def __add__(self, other):
        """Add two Vectors."""
        if isinstance(other, Vector) and len(self.components) == len(other.components):
            added_components = tuple(a + b for a, b in zip(self.components, other.components))
            return Vector(*added_components)
        return NotImplemented

    def __len__(self):
        """Return the number of components in the Vector."""
        return len(self.components)

    def __getitem__(self, index):
        """Allow indexing to access components of the Vector."""
        return self.components[index]

    def __eq__(self, other):
        """Compare two Vectors for equality."""
        if isinstance(other, Vector):
            return self.components == other.components
        return False

    def __lt__(self, other):
        """Compare two Vectors for less-than relationship."""
        if isinstance(other, Vector):
            return self.magnitude() < other.magnitude()
        return NotImplemented

    def __le__(self, other):
        """Compare two Vectors for less-than-or-equal relationship."""
        if isinstance(other, Vector):
            return self.magnitude() <= other.magnitude()
        return NotImplemented

    def magnitude(self):
        """Calculate and return the magnitude of the Vector."""
        return sum(x ** 2 for x in self.components) ** 0.5

    def __del__(self):
        """Called when the Vector is about to be destroyed."""
        print(f"Vector{self.components} is being deleted.")


# Example usage:
v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)

print(repr(v1))          # Output: Vector(1, 2, 3)
print(str(v1))           # Output: Vector with components: (1, 2, 3)

v3 = v1 + v2
print(v3)                # Output: Vector with components: (5, 7, 9)

print(len(v1))           # Output: 3
print(v1[1])             # Output: 2 (uses the "__getitem__" dunder method)

print(v1 == v2)          # Output: False
print(v1 < v2)           # Output: True

# Deleting a vector
del v1

# also if "del v1" isn't written, it will be called automatically at the end of the program.
# That's why v2 and v3 are also deleted at the end of the program.
