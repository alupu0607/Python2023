class Matrix:
    def __init__(self, n, m, initial_values = None):
        self.n = n  
        self.m = m 
        if initial_values is not None:
            if len(initial_values) != n or any(len(row) != m for row in initial_values):
                raise ValueError("Invalid dimensions for initial values")
            self.data = initial_values
        else:
            self.data = [[0] * m for _ in range(n)]

    def get(self, i, j):
        if 0 <= i < self.n and 0 <= j < self.m:
            return self.data[i][j]
        else:
            return None

    def set(self, i, j, value):
        if 0 <= i < self.n and 0 <= j < self.m:
            self.data[i][j] = value

    def transpose(self):
        transposed = Matrix(self.m, self.n)
        for i in range(self.n):
            for j in range(self.m):
                transposed.data[j][i] = self.data[i][j]
        return transposed

    def multiply(self, other):
        if self.m != other.n:
            return None  
        result = Matrix(self.n, other.m)
        for i in range(self.n):
            for j in range(other.m):
                for k in range(self.m):
                    result.data[i][j] += self.data[i][k] * other.data[k][j]
        return result

    def apply(self, func):
        for i in range(self.n):
            for j in range(self.m):
                self.data[i][j] = func(self.data[i][j])

    def __str__(self):
        return "\n".join(["\t".join(map(str, row)) for row in self.data])

matrix = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])

print("Original Matrix:")
print(matrix)

transposed_matrix = matrix.transpose()
print("\nTransposed Matrix:")
print(transposed_matrix)

identity_matrix = Matrix(3, 3, [[1,0,0], [0,1,0], [0,0,1]])

product_matrix = matrix.multiply(identity_matrix)
print("\nMatrix Multiplication Result:")
print(product_matrix)

matrix.apply(lambda x: x * 2)
print("\nMatrix After Applying Transformation:")
print(matrix)
