def join(vector1, vector2):
    if len(vector1) != len(vector2):
        return None
    return [e1 | e2 for e1, e2 in zip(vector1, vector2)]


def meet(vector1, vector2):
    if len(vector1) != len(vector2):
        return None
    return [e1 & e2 for e1, e2 in zip(vector1, vector2)]


def transpose(matrix):
    width = len(matrix[0])

    transpose_matrix = [[]] * width
    for i in range(width):
        transpose_matrix[i] = [vector[i] for vector in matrix]

    return transpose_matrix


def space(matrix):
    space = set([tuple(vector) for vector in matrix])

    n = len(matrix)
    m = len(matrix[0])

    for i in range(n):
        for j in range(i+1, n):
            space.add(tuple(join(matrix[i], matrix[j])))

    space.add((0,) * m)

    return space


def column_space(matrix):
    transpose_matrix = transpose(matrix)
    return space(transpose_matrix)


def row_space(matrix):
    return space(matrix)


def comparable(vector1, vector2):
    if all(x <= y for x, y in zip(vector1, vector2)) or \
            all(x >= y for x, y in zip(vector1, vector2)):
        return True
    return False


def lattice(space):
    n = len(space)

    lattice = list()

    for i in range(n):
        lattice.append(list())
        for j in range(n):
            if i == j:
                lattice[i].append(1)
            elif comparable(space[i], space[j]):
                lattice[i].append(1)
            else:
                lattice[i].append(0)

    return lattice


def isomorphic(lattice1, lattice2):
    unordered_degree_sequnce1 = [sum(row) for row in lattice1]
    unordered_degree_sequnce2 = [sum(row) for row in lattice2]
    if unordered_degree_sequnce1[0] != unordered_degree_sequnce2[0]:
        return False
    return sorted(unordered_degree_sequnce1) == sorted(unordered_degree_sequnce2)


def multiplication(matrix1, matrix2):
    if len(matrix1[0]) != len(matrix2):
        return None

    n = len(matrix1)
    m = len(matrix2[1])

    result = list()
    for i in range(m):
        result.append([0] * n)

    for i in range(n):
        for j in range(m):
            v1 = matrix1[i]
            v2 = [v[j] for v in matrix2]
            result[i][j] = int(any(meet(v1, v2)))

    return result


def get_matrix(matrix):
    from app.models import Matrix

    h = len(matrix)
    w = len(matrix[0])

    body = 0
    for i in range(h):
        for j in range(w):
            body |= ((1 & matrix[i][j]) << (h * w - (i * w + j) - 1))

    return Matrix.query.filter(Matrix.height == h, Matrix.width == w,
                               Matrix.body == body).first()
