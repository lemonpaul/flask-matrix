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
    vectors = list(matrix)
    null_vector = [0] * len(vectors[0])
    if null_vector not in vectors:
        vectors.append(null_vector)

    return set(tuple(vector) for vector in vectors)
