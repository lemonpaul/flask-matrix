import time

from math import ceil, log

from app import create_app, db
from app.models import Matrix, H_class, L_class, R_class, D_class
from app.utils import get_matrix, row_space, column_space, find_alchemy_matrix

app = create_app()
app.app_context().push()


def init_matrices(height, width, n_threads):
    h_classes = []

    for h in range(1, height+1):
        for w in range(1, width+1):
            matrices = []

            for b in range(0, 1 << w*h):
                matrix = get_matrix(h, w, b)
                matrices.append(matrix)

                alchemy_matrix = Matrix(width=w, height=h, body=b)
                db.session.add(alchemy_matrix)

            print(f'{w}x{h} matrices. {len(matrices)} matrices.')

            size_h_classes = []

            for matrix in matrices:
                for h_class in size_h_classes:
                    class_matrix = h_class[0]
                    if row_space(matrix) == row_space(class_matrix) and \
                            column_space(matrix) == column_space(class_matrix):
                        h_class.append(matrix)
                        break
                else:
                    h_class = [matrix]
                    size_h_classes.append(h_class)
           
            h_classes.extend(size_h_classes)

    l_classes = []

    for h_class in h_classes:
        matrix = h_class[0]

        for l_class in l_classes:
            class_matrix = l_class[0]
            if row_space(matrix) == row_space(class_matrix):
                l_class.extend(h_class)
                break
        else:
            l_class = h_class
            l_classes.append(l_class)

    r_classes = []

    for h_class in h_classes:
        matrix = h_class[0]

        for r_class in r_classes:
            class_matrix = r_class[0]
            if column_space(matrix) == column_space(class_matrix):
                r_class.extend(h_class)
                break
        else:
            r_class = h_class
            r_classes.append(r_class)

    d_classes = []

    for l_class in l_classes:
        matrix = l_class[0]
        for d_class in d_classes:
            class_matrix = d_class[0]

            matrix_r_class = next(filter(lambda r_class: matrix in r_class, r_classes))

            class_matrix_l_class = next(filter(lambda l_class: class_matrix in l_class, l_classes))

            if set(matrix_r_class) & set(class_matrix_l_class):
                d_class.extend(l_class.matrices)
                break
        else:
            d_class = []
            d_class.extend(l_class)
            d_classes.append(d_class)

    db.session.commit()


def init(height=3, width=3, n_threads=8):
    Matrix.query.delete()
    H_class.query.delete()
    L_class.query.delete()
    R_class.query.delete()
    D_class.query.delete()
    db.session.commit()

    start = time.time()
    init_matrices(height, width, n_threads)
    return time.time() - start
