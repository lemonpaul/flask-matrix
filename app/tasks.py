import time

from math import ceil, log

from app import create_app, db
from app.models import Matrix, H_class, L_class, R_class, D_class
from app.utils import get_matrix, row_space, column_space, find_alchemy_matrix, as_set

app = create_app()
app.app_context().push()


def clear():
    Matrix.query.delete()
    H_class.query.delete()
    L_class.query.delete()
    R_class.query.delete()
    D_class.query.delete()
    db.session.commit()


def init_data(height, width, n_threads):

    # Initialize alchemy matrices and compute H-classes

    h_classes = []

    for h in range(1, height+1):
        for w in range(1, width+1):
            matrices = []

            print(f'Initialing {1 << w*h} {w}x{h} matrices...')

            for b in range(0, 1 << w*h):
                matrix = get_matrix(h, w, b)
                matrices.append(matrix)

                alchemy_matrix = Matrix(width=w, height=h, body=b)
                db.session.add(alchemy_matrix)

            print(f'Computing H-classes for {w}x{h} matrices...')

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

    print(f'Computing L-classes...')

    l_classes = []

    for h_class in h_classes:
        matrix = h_class[0]

        for l_class in l_classes:
            class_matrix = l_class[0]
            if row_space(matrix) == row_space(class_matrix):
                l_class.extend(h_class)
                break
        else:
            l_class = []
            l_class.extend(h_class)
            l_classes.append(l_class)

    print(f'Computing R-classes...')

    r_classes = []

    for h_class in h_classes:
        matrix = h_class[0]

        for r_class in r_classes:
            class_matrix = r_class[0]
            if column_space(matrix) == column_space(class_matrix):
                r_class.extend(h_class)
                break
        else:
            r_class = []
            r_class.extend(h_class)
            r_classes.append(r_class)

    print(f'Computing D-classes...')

    d_classes = []

    for l_class in l_classes:
        matrix = l_class[0]
        for d_class in d_classes:
            class_matrix = d_class[0]

            r_class = next(filter(lambda r_class: class_matrix in r_class, r_classes))

            if as_set(l_class) & as_set(r_class):
                d_class.extend(l_class)
                break
        else:
            d_class = []
            d_class.extend(l_class)
            d_classes.append(d_class)
    
    print(f'Storing H-classes in database...')

    for h_class in h_classes:
        cls = H_class()
        for matrix in h_class:
            mtx = find_alchemy_matrix(matrix)
            mtx.h_class = cls

    print(f'Storing L-classes in database...')

    for l_class in l_classes:
        cls = L_class()
        for matrix in l_class:
            mtx = find_alchemy_matrix(matrix)
            mtx.l_class = cls

    print(f'Storing R-classes in database...')

    for r_class in r_classes:
        cls = R_class()
        for matrix in r_class:
            mtx = find_alchemy_matrix(matrix)
            mtx.r_class = cls

    print(f'Storing D-classes in database...')

    for d_class in d_classes:
        cls = D_class()
        for matrix in d_class:
            mtx = find_alchemy_matrix(matrix)
            mtx.d_class = cls

    db.session.commit()


def init(height=3, width=3, n_threads=8):
    clear()

    start = time.time()
    init_data(height, width, n_threads)
    return time.time() - start
