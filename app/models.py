from app import db
from app.utils import basis, transpose


class Matrix(db.Model):
    __tablename__ = 'matrices'
    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    body = db.Column(db.Integer)

    def to_array(self):
        data = [[]] * self.height
        for k in range(self.height):
            data[k] = [0] * self.width
        for i in range(self.height):
            for j in range(self.width):
                shift = self.width * self.height - (i * self.width + j) - 1
                if 1 << shift & self.body:
                    data[i][j] = 1
        return data

    def column_space(self):
        matrix = self.to_array()
        return basis(matrix)

    def row_space(self):
        matrix = transpose(self.to_array())
        return basis(matrix)

    def __repr__(self):
        return '<Matrix {}x{}>'.format(self.width, self.height)
