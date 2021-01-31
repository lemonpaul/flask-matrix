import time
from app import create_app, db
from app.models import Matrix, H_class, L_class, R_class, D_class

app = create_app()
app.app_context().push()


def init_matrices(height=3, width=3, max_batch_size=512):
    for h in range(1, height+1):
        for w in range(1, width + 1):
            for body in range(0, 1 << w*h):
                matrix = Matrix(width=w, height=h, body=body)
                db.session.add(matrix)

    for matrix_i in Matrix.query.all():
        h_class = H_class()
        for matrix_j in Matrix.query.filter(Matrix.height == matrix_i.width):
            pass

    for h in range(1, height+1):
        for w in range(1, width + 1):
            matrices = Matrix.query.filter(Matrix.width == w, Matrix.height == h).all()
            matrix_length = matrices.__len__()
            batch_size = min(matrix_length, max_batch_size)
            batch_length = int(matrix_length / batch_size)
            print(f'{w}x{h} matrices. {batch_length} batches.')
            batches = []
            for n_batch in range(0, batch_length):
                print(f'Fill batch {n_batch+1}/{batch_length}...')
                batches.append([])
                for matrix in matrices[n_batch*batch_size:(n_batch+1)*batch_size]:
                    for h_class in batches[n_batch]:
                        class_matrix = h_class.matrices[0]
                        if matrix.row_space() == class_matrix.row_space() and matrix.column_space() == class_matrix.column_space():
                            h_class.matrices.append(matrix)
                            break
                    else:
                        matrix.h_class = H_class()
                        batches[n_batch].append(matrix.h_class)

            all_h_classes = []
            if batch_length > 1:
                n_batch = 1
                for batch in batches:
                    print(f'Process batch {n_batch}/{batch_length}, {len(batch)} H-classes...')

                    for batch_h_class in batch:
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

                    n_batch += 1

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


def init(height=3, width=3, max_batch_size=512):
    Matrix.query.delete()
    H_class.query.delete()
    L_class.query.delete()
    R_class.query.delete()
    D_class.query.delete()
    db.session.execute("ALTER SEQUENCE matrix_id_seq RESTART WITH 1")
    db.session.execute("ALTER SEQUENCE h_class_id_seq RESTART WITH 1")
    db.session.execute("ALTER SEQUENCE l_class_id_seq RESTART WITH 1")
    db.session.execute("ALTER SEQUENCE r_class_id_seq RESTART WITH 1")
    db.session.execute("ALTER SEQUENCE d_class_id_seq RESTART WITH 1")
    db.session.commit()

    start = time.time()
    init_matrices(height, width, max_batch_size)
    return time.time() - start
