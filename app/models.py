from app import db

class Matrix(db.Model):
    __tablename__ = 'matrices'
    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    body = db.Column(db.Integer)

    def to_array(self):
        data=[[]] * self.height
        for k in range(self.height):
            data[k] = [0] * self.width
        for i in range(self.height):
            for j in range(self.width):
                shift = self.width * self.height - (i * self.width + j) - 1
                print(f'shift={shift}, i={i}, j={j}: {1 << shift & self.body}')
                if 1 << shift & self.body:
                    data[i][j] = 1
        return data


    def __repr__(self):
        return '<Matrix {}x{}>'.format(self.width, self.height)
