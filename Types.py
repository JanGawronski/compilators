class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def __str__(self):
        return "\n".join(self.matrix)

    def element_by_element(self, other, function):
        return [[function(self.matrix, other, i, j) for i in range(len(self.matrix[0]))] for j in range(len(self.matrix))]

    def __add__(self, other):
        return self.element_by_element(self, other, lambda m, o, i, j: m[i][j] + o.matrix[i][j])

    def __mul__(self, other):
        res = [[0 for _ in range(len(self.matrix[0]))] for _ in range(len(self.matrix))]

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                for k in range(len(other.matrix[0])):
                    res[i][k] = self.matrix[i][j] * other.matrix[j][k]

        return res
    
    def __sub__(self, other):
        return self.element_by_element(self, other, lambda m, o, i, j: m[i][j] - o.matrix[i][j])

    def scalar_mul(self, other):
        return self.element_by_element(self, other, lambda m, o, i, j: m[i][j] * o)

    def scalar_div(self, other):
        return self.element_by_element(self, other, lambda m, o, i, j: m[i][j] / o)

    def ebe_mul(self, other):
        return self.element_by_element(self, other, lambda m, o, i, j: m[i][j] + o.matrix[i][j])

    @staticmethod
    def matrix_function(self, function, n, m = -1)
        if m == -1:
            m = n

        return [[function(i, j) for i in range(n)] for j in range(m)]
    

    @staticmethod
    def ones(self, n, m = -1):
        return Matrix.matrix_function(lambda i, j: 1 if i == j else 0, n, m)
        


class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start}..{self.end}"