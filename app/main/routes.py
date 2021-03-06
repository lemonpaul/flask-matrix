import base64
import networkx as nx
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from io import BytesIO
from app import db
from app.main import bp
from app.models import Matrix, intersection, width, height
from flask import render_template, request, url_for, current_app, send_file
from importlib import import_module
from app.tasks import app
from matplotlib.figure import Figure

app.app_context().push()


@bp.route('/')
def index():
    return render_template('index.html', title='Home')


@bp.route('/theory')
def theory():
    return render_template('theory.html', title='Theory')


@bp.route('/matrix')
def matrix_index():
    page = request.args.get('page', 1, type=int)
    matrices = Matrix.query.paginate(
        page, current_app.config['MATRICES_PER_PAGE'], False
    )
    next_url = url_for('main.matrix_index', page=matrices.next_num) \
        if matrices.has_next else None
    prev_url = url_for('main.matrix_index', page=matrices.prev_num) \
        if matrices.has_prev else None
    return render_template('matrix/index.html', title='Matrices', matrices=matrices.items,
                           page=matrices.page, pages=matrices.pages, per_page=matrices.per_page, total=matrices.total,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/poset')
def poset():
    G = nx.complete_graph(5)
    nx.draw(G)

    img = BytesIO() # file-like object for the image
    plt.savefig(img, format='png') # save the image to the stream
    plt.clf()

    data = base64.b64encode(img.getbuffer()).decode("ascii")
    return render_template('poset.html', title='Partial order set of D-classes', data=data)


@bp.route('/explore/<string:class_name>')
def explore_index(class_name):
    from app.models import D_class

    d_classes = D_class.query.all()
    return render_template('explore/index.html', title=class_name+'-classes',
                           d_classes=d_classes, intersection=intersection, class_name=class_name,
                           height=height, width=width)


@bp.route('/explore/<string:class_name>/<int:class_id>')
def explore_show(class_name, class_id):
    width = int(request.args.get('width'))
    height = int(request.args.get('height'))
    size = int(request.args.get('size'))

    model = getattr(import_module('app.models'), class_name+'_class')

    matrices = model.query.get(class_id).matrices

    return render_template('explore/show.html', matrices=matrices, width=width, height=height, size=size)


@bp.route('/class/<string:class_name>/<int:class_id>')
def class_show(class_name, class_id):
    model = getattr(import_module('app.models'), class_name+'_class')

    page = request.args.get('page', 1, type=int)
    matrices = db.session.query(Matrix).join(model).filter(model.id == class_id).paginate(
        page, current_app.config['MATRICES_PER_PAGE'], False
    )
    next_url = url_for('main.class_show', class_name=class_name, class_id=class_id, page=matrices.next_num) \
        if matrices.has_next else None
    prev_url = url_for('main.class_show', class_name=class_name, class_id=class_id, page=matrices.prev_num) \
        if matrices.has_prev else None

    return render_template('class/show.html', class_name=class_name, matrices=matrices.items,
                           page=matrices.page, pages=matrices.pages, per_page=matrices.per_page, total=matrices.total,
                           next_url=next_url, prev_url=prev_url)
