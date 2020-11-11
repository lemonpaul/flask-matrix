from app import db
from app.utils import basis, transpose
from sqlalchemy.orm import relationship


class Matrix(db.Model):
    __tablename__ = 'matrix'
    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    body = db.Column(db.Integer)
    h_class_id = db.Column(db.Integer, db.ForeignKey('h_class.id'))
    h_class = relationship('H_class', back_populates='matrices')

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


class H_class(db.Model):
    __tablename__ = 'h_class'
    id = db.Column(db.Integer, primary_key=True)
    matrices = relationship('Matrix', back_populates='h_class')
    l_class_id = db.Column(db.Integer, db.ForeignKey('l_class.id'))
    l_class = relationship('L_class', back_populates='h_classes')
    r_class_id = db.Column(db.Integer, db.ForeignKey('r_class.id'))
    r_class = relationship('R_class', back_populates='h_classes')


class L_class(db.Model):
    __tablename__ = 'l_class'
    id = db.Column(db.Integer, primary_key=True)
    h_classes = relationship('H_class', back_populates='l_class')
    d_class_Id = db.Column(db.Integer, db.ForeignKey('d_class.id'))
    d_class = relationship('D_class', back_populates='l_classes')


class R_class(db.Model):
    __tablename__ = 'r_class'
    id = db.Column(db.Integer, primary_key=True)
    h_classes = relationship('H_class', back_populates='r_class')
    d_class_Id = db.Column(db.Integer, db.ForeignKey('d_class.id'))
    d_class = relationship('D_class', back_populates='r_classes')


class D_class(db.Model):
    __tablename__ = 'd_class'
    id = db.Column(db.Integer, primary_key=True)
    l_classes = relationship('L_class', back_populates='d_class')
    r_classes = relationship('R_class', back_populates='d_class')
