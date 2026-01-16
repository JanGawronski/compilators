class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def __str__(self):
        return "\n".join([str(v) for v in self.matrix])

    def element_by_element(self, other, function):
        return Matrix([[function(self.matrix, other, i, j) for i in range(len(self.matrix[0]))] for j in range(len(self.matrix))])

    def __add__(self, other):
        return self.element_by_element(other, lambda m, o, i, j: m[i][j] + o.matrix[i][j])
            
    def __sub__(self, other):
        return self.element_by_element(other, lambda m, o, i, j: m[i][j] - o.matrix[i][j])

    def __mul__(self, other):
        if type(other) == Matrix:
            res = [[0 for _ in range(len(self.matrix[0]))] for _ in range(len(self.matrix))]

            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    for k in range(len(other.matrix[0])):
                        res[i][k] = self.matrix[i][j] * other.matrix[j][k]

            return res
        else:
            return self.element_by_element(other, lambda m, o, i, j: m[i][j] * o)

    def __div__(self, other):
        if type(other) == Matrix:
             return self.element_by_element(other, lambda m, o, i, j: m[i][j] / o.matrix[i][j])
        else:
            return self.element_by_element(other, lambda m, o, i, j: m[i][j] / o)

    def ebe_mul(self, other):
        return self.element_by_element(other, lambda m, o, i, j: m[i][j] * o.matrix[i][j])

    def transpose(self):
        return Matrix([[self.matrix[i][j] for j in range(len(self.matrix))] for i in range(self.matrix[0])])

    def get(self, i, j=None):
        if type(i) == Range:
            first = self.matrix[i.start : i.end + 1]
            if j is None:
                return Matrix(first)
            if type(j) == Range:
                return Matrix(first[j.start : j.end + 1])
            return Vector(first[i])
        else:
            first = self.matrix[i]
            if j is None:
                return Vector(first)
            if type(j) == Range:
                return Vector(first[j.start : j.end + 1])
            return first[j]

    def set(self, value, i, j=None):
        if type(value) not in [Matrix, Vector]:
            self.matrix[i][j] = value
            return
            
        first_dim = list(range(i.start, i.end + 1)) if type(i) == Range else [i]
        if j is None:
            for v, x in enumerate(first_dim):
                self.matrix[x] = value.get(v)
            return
        second_dim = list(range(j.start, j.end + 1)) if type(j) == Range else [j]
        for v, x in enumerate(first_dim):
            for w, y in enumerate(second_dim):
                self.matrix[y][x] = value.get(w, v)
        
    @staticmethod
    def matrix_function(function, n, m = -1):
        if m == -1:
            m = n

        return Matrix([[function(i, j) for i in range(n)] for j in range(m)])

    @staticmethod
    def ones(n, m = -1):
        return Matrix.matrix_function(lambda i, j: 1, n, m)

    @staticmethod
    def zeros(n, m = -1):
        return Matrix.matrix_function(lambda i, j: 0, n, m)
 
    @staticmethod
    def eye(n, m = -1):
        return Matrix.matrix_function(lambda i, j: 1 if i == j else 0, n, m)
        
class Vector:
    def __init__(self, vector):
       self.vector = vector

    def __str__(self):
        return str(self.vector) 

    def element_by_element(self, other, function):
        return Vector([function(self.vector, other, i) for i in range(len(self.vector[0]))])

    def __add__(self, other):
        return self.element_by_element(other, lambda v, o, i: v[i] + o.vector[i])

    def __sub__(self, other):
        return self.element_by_element(other, lambda v, o, i: v[i] - o.vector[i])

    def __mul__(self, other):
        if type(other) == Vector:
            return self.element_by_element(other, lambda v, o, i: v[i] * o.vector[i])
        else:            
            return self.element_by_element(other, lambda v, o, i: v[i] * o)
        
    def __div__(self, other):
        if type(other) == Vector:
            return self.element_by_element(other, lambda v, o, i: v[i] / o.vector[i])
        else:
            return self.element_by_element(other, lambda v, o, i: v[i] / o)

    def ebe_mul(self, other):
        return self * other

    def get(self, i):
        if type(i) == Range:
            return Vector(self.vector[i.start : i.end + 1])
        else:
            return self.vector[i]
 
    def set(self, value, i):
        if type(i) == Range:
            self.vector[i.start : i.end + 1] = value.vector
        else:
            self.vector[i] = value
    
class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start}:{self.end}"
