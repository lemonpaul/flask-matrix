import time
from app import create_app, db
from app.models import Matrix, H_class, L_class, R_class, D_class

app = create_app()
app.app_context().push()


def init_matrices(height=3, width=3):
    for h in range(1, height+1):
        for w in range(1, width + 1):
            for body in range(0, 1 << w*h):
                matrix = Matrix(width=w, height=h, body=body)
                db.session.add(matrix)

    for matrix in Matrix.query.all():
        for h_class in H_class.query.all():
            class_matrix = h_class.matrices[0]
            if matrix.row_space() == class_matrix.row_space() and matrix.column_space() == class_matrix.column_space():
                class_matrix.h_class.matrices.append(matrix)
                break
        else:
            matrix.h_class = H_class()

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
            db.session.add(class_)

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
            db.session.add(class_)

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
            db.session.add(class_)

    db.session.commit()


def init(height=3, width=3):
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

    start_time = time.time()
    init_matrices(height, width)
    print(f'Elapsed time: {(time.time() - start_time):.2f}')
