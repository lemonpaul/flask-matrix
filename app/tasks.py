from app import create_app, db
from app.models import Matrix, H_class, L_class, R_class

app = create_app()
app.app_context().push()


def init_matrices(height=3, width=3):
    for h in range(1, height+1):
        for w in range(1, width + 1):
            for body in range(0, 1 << w*h):
                matrix = Matrix(width=w, height=h, body=body)
                db.session.add(matrix)

    db.session.commit()


def clear_matrices():
    Matrix.query.delete()
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

def clear_h_classes():
    H_class.query.delete()
    db.session.commit()

def init_l_classes():
    for h_class in H_class.query.all():
        for l_class in L_class.query.all():
            l_h_class = l_class.h_classes[0]
            if h_class.matrices[0].row_space() == l_h_class.matrices[0].row_space():
                l_class.h_classes.append(h_class)
                break
        else:
            l_class = L_class()
            l_class.h_classes.append(h_class)
            db.session.add(l_class)
    db.session.commit()


def init_r_classes():
    for h_class in H_class.query.all():
        for r_class in R_class.query.all():
            r_h_class = r_class.h_classes[0]
            if h_class.matrices[0].row_space() == r_h_class.matrices[0].row_space():
                r_class.h_classes.append(h_class)
                break
        else:
            r_class = R_class()
            r_class.h_classes.append(h_class)
            db.session.add(r_class)
    db.session.commit()

