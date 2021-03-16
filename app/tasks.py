import time

from math import ceil, log

from app import create_app, db
from app.models import Matrix, H_class, L_class, R_class, D_class

app = create_app()
app.app_context().push()


def init_matrices(height, width, n_threads):
    for h in range(1, height+1):
        for w in range(1, width + 1):
            for body in range(0, 1 << w*h):
                matrix = Matrix(width=w, height=h, body=body)
                db.session.add(matrix)

    for h in range(1, height+1):
        for w in range(1, width + 1):
            matrices = Matrix.query.filter(Matrix.width == w, Matrix.height == h).all()
            n_matrices = matrices.__len__()
            if n_matrices / n_threads > 1:
                s_batch = 2 ** ceil(log(n_matrices/n_threads, 2))
            else:
                s_batch = n_matrices
            n_batches = int(n_matrices / s_batch)
            print(f'{w}x{h} matrices. {n_batches} batches.')
            batches = []
            for idx_batch in range(0, n_batches):
                print(f'Fill batch {idx_batch+1}/{n_batches}...')
                batches.append([])
                for matrix in matrices[idx_batch*s_batch:(idx_batch+1)*s_batch]:
                    for h_class in batches[idx_batch]:
                        class_matrix = h_class.matrices[0]
                        if matrix.row_space() == class_matrix.row_space() and matrix.column_space() == class_matrix.column_space():
                            h_class.matrices.append(matrix)
                            break
                    else:
                        matrix.h_class = H_class()
                        batches[idx_batch].append(matrix.h_class)

            if n_batches > 1:
                all_h_classes = []
                idx_batch = 0
                for idx_batch in range(0, n_batches):
                    print(f'Process batch {idx_batch+1}/{n_batches}, {len(batches[idx_batch])} H-classes...')

                    for batch_h_class in batches[idx_batch]:
                        matrix = batch_h_class.matrices[0]
                        for h_class in all_h_classes:
                            class_matrix = h_class.matrices[0]
                            if matrix.row_space() == class_matrix.row_space() and matrix.column_space() == class_matrix.column_space():
                                h_class.matrices.extend(list(batch_h_class.matrices))
                                all_h_classes.append(h_class)
                                db.session.expunge(batch_h_class)
                                break
                        else:
                            all_h_classes.append(batch_h_class)

    for h_class in H_class.query.all():
        matrix = h_class.matrices[0]
        for l_class in L_class.query.all():
            class_matrix = l_class.matrices[0]
            if matrix.row_space() == class_matrix.row_space():
                class_matrix.l_class.matrices.extend(h_class.matrices)
                break
        else:
            class_ = L_class()
            class_.matrices.extend(h_class.matrices)

    for h_class in H_class.query.all():
        matrix = h_class.matrices[0]
        for r_class in R_class.query.all():
            class_matrix = r_class.matrices[0]
            if matrix.column_space() == class_matrix.column_space():
                class_matrix.r_class.matrices.extend(h_class.matrices)
                break
        else:
            class_ = R_class()
            class_.matrices.extend(h_class.matrices)

    for l_class in L_class.query.all():
        matrix = l_class.matrices[0]
        for d_class in D_class.query.all():
            class_matrix = d_class.matrices[0]
            if set(matrix.r_class.matrices) & set(class_matrix.l_class.matrices):
                class_matrix.d_class.matrices.extend(l_class.matrices)
                break
        else:
            class_ = D_class()
            class_.matrices.extend(l_class.matrices)

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
