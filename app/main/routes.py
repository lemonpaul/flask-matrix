from app import db
from app.main import bp
from app.models import Matrix, intersection
from flask import render_template, request, url_for, current_app
from importlib import import_module
from app.tasks import app

app.app_context().push()


@bp.route('/')
def index():
    return render_template('index.html', title='Home')


@bp.route('/explore')
def explore():
    from app.models import D_class, L_class
    d_classes = D_class.query.all()
    total = L_class.query.count()
    return render_template('explore.html', title='Structure', d_classes=d_classes, intersection=intersection, total=total)


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


@bp.route('/class/<string:class_name>')
def class_index(class_name):
    model = getattr(import_module('app.models'), class_name+'_class')
    classes = model.query.all()

    return render_template('class/index.html', class_name=class_name, classes=classes)


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
