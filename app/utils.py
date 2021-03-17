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
    space_ = set([tuple(vector) for vector in matrix])

    n = len(matrix)
    m = len(matrix[0])

    for i in range(n):
        for j in range(i+1, n):
            space_.add(tuple(join(matrix[i], matrix[j])))

    space_.add((0,) * m)

    return space_


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


def lattice(space_):
    n = len(space_)

    lattice_ = list()

    for i in range(n):
        lattice_.append(list())
        for j in range(n):
            if i == j:
                lattice_[i].append(1)
            elif comparable(space[i], space[j]):
                lattice_[i].append(1)
            else:
                lattice_[i].append(0)

    return lattice_


def isomorphic(lattice1, lattice2):
    unordered_degree_sequence1 = [sum(row) for row in lattice1]
    unordered_degree_sequence2 = [sum(row) for row in lattice2]
    if unordered_degree_sequence1[0] != unordered_degree_sequence2[0]:
        return False
    return sorted(unordered_degree_sequence1) == sorted(unordered_degree_sequence2)


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


def intersection(l_class_id_1, l_class_id_2):
    from app.models import Matrix, L_class

    set_1 = {matrix.id for matrix in L_class.query.get(l_class_id_1).matrices}
    set_2 = {matrix.id for matrix in L_class.query.get(l_class_id_2).matrices}

    meet_set = set_1 & set_2

    return Matrix.query.filter(Matrix.id.in_(meet_set))


def find_alchemy_matrix(matrix):
    from app.models import Matrix

    h = len(matrix)
    w = len(matrix[0])

    body = 0
    for i in range(h):
        for j in range(w):
            body |= ((1 & matrix[i][j]) << (h * w - (i * w + j) - 1))

    return Matrix.query.filter(Matrix.height == h, Matrix.width == w,
                               Matrix.body == body).first()

def get_matrix(height, width, body):
    data = [[]] * height
    for k in range(height):
        data[k] = [0] * width
    for i in range(height):
        for j in range(width):
            shift = width * height - (i * width + j) - 1
            if 1 << shift & body:
                data[i][j] = 1
    return data
