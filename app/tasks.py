from app import create_app, db
from app.models import Matrix

app = create_app()
app.app_context().push()

def init_matrices(height=3, width=3):
    for h in range(1, height+1):
        for w in range(1, width+1):
            for body in range(0, 1<<w*h):
                matrix = Matrix(width=w, height=h, body=body)
                db.session.add(matrix)

    db.session.commit()

def clear_matrices():
    Matrix.query.delete()
    db.session.commit()
