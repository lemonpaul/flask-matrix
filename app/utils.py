def sum(vector1, vector2):
    length = len(vector1)
    if len(vector2) != length:
        return
    result = [0] * length
    for i in range(length):
        if vector1[i] + vector2[i] > 0:
            result[i] = 1
    return result


def sub(vector1, vector2):
    length = len(vector1)
    if len(vector2) != length:
        return
    result = [0] * length
    for i in range(length):
        if vector1[i] == 1 and vector2[i] == 0:
            result[i] = 1
        elif vector1[i] == 0 and vector2[i] == 1:
            return vector1
    return result


def transpose(matrix):
    width = len(matrix[0])

    transpose_matrix = [[]] * width
    for i in range(width):
        transpose_matrix[i] = [vector[i] for vector in matrix]

    return transpose_matrix


def basis(matrix):
    height = len(matrix)
    width = len(matrix[0])

    for index in range(min(height, width)):
        for column_number in range(index+1, height):
            if matrix[column_number][index] == 1:
                matrix[index], matrix[column_number] = matrix[column_number], matrix[index]
                break

        for column_number in range(height):
            if column_number != index:
                matrix[column_number] = sub(matrix[column_number], matrix[index])

    basis_set = set()
    for vector in matrix:
        basis_set.add(tuple(vector))
    basis_set.add((0,) * width)

    basis_list = [list(tuple) for tuple in basis_set]

    return basis_list
