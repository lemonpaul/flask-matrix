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

    db.session.commit()


def init_h_classes():
    for matrix in Matrix.query.all():
        for h_class in H_class.query.all():
            class_matrix = h_class.matrices[0]
            if matrix.column_space() == class_matrix.column_space() and matrix.row_space() == class_matrix.row_space():
                h_class.matrices.append(matrix)
                break
        else:
            h_class = H_class()
            h_class.matrices.append(matrix)
            db.session.add(h_class)
    db.session.commit()


def init_l_classes():
    for matrix in Matrix.query.all():
        for l_class in L_class.query.all():
            class_matrix = l_class.matrices[0]
            if matrix.row_space() == class_matrix.row_space():
                l_class.matrices.append(matrix)
                break
        else:
            l_class = L_class()
            l_class.matrices.append(matrix)
            db.session.add(l_class)
    db.session.commit()


def init_r_classes():
    for matrix in Matrix.query.all():
        for r_class in R_class.query.all():
            class_matrix = r_class.matrices[0]
            if matrix.column_space() == class_matrix.column_space():
                r_class.matrices.append(matrix)
                break
        else:
            r_class = R_class()
            r_class.matrices.append(matrix)
            db.session.add(r_class)
    db.session.commit()


def init_d_classes():
    for matrix in Matrix.query.all():
        for d_class in D_class.query.all():
            class_matrix = d_class.matrices[0]
            if matrix.column_space() == class_matrix.column_space() or matrix.row_space() == class_matrix.row_space():
                d_class.matrices.append(matrix)
                break
        else:
            d_class = D_class()
            d_class.matrices.append(matrix)
            db.session.add(d_class)
    db.session.commit()


def init():
    Matrix.query.delete()
    H_class.query.delete()
    L_class.query.delete()
    R_class.query.delete()
    D_class.query.delete()
    db.session.commit()
    init_matrices()
    init_h_classes()
    init_l_classes()
    init_r_classes()
    init_d_classes()
