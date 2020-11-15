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


def isomorphic(matrix1, matrix2):
    matrix1_row_space = list(list(tuple) for tuple in space(matrix1))
    min_matrix1_isomporphic = space(transpose(matrix1_row_space))
    matrix2_row_space = list(list(tuple) for tuple in space(matrix2))
    min_matrix2_isomporphic = space(transpose(matrix2_row_space))
    return min_matrix1_isomporphic == min_matrix2_isomporphic
