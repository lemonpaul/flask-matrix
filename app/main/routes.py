from app.main import bp
from app.models import Matrix, H_class, L_class, R_class, D_class
from flask import render_template, request, url_for, current_app


@bp.route('/')
def index():
    return render_template('index.html', title='Home')


@bp.route('/explore')
def explore():
    return render_template('explore.html', title='Theory')


@bp.route('/matrices')
def matrices():
    page = request.args.get('page', 1, type=int)
    matrices = Matrix.query.paginate(
        page, current_app.config['MATRICES_PER_PAGE'], False
    )
    first_url = url_for('main.matrices', page=1)
    last_url = url_for('main.matrices', page=matrices.pages)
    next_url = url_for('main.matrices', page=matrices.next_num) \
        if matrices.has_next else None
    prev_url = url_for('main.matrices', page=matrices.prev_num) \
        if matrices.has_prev else None
    return render_template('matrices.html', title='Matrices', matrices=matrices.items,
                           page=matrices.page, pages=matrices.pages, per_page=matrices.per_page, total=matrices.total,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/h_classes')
def h_classes():
    h_classes = H_class.query.all()
    return render_template('h_classes.html', title='H classes', h_classes=h_classes)


@bp.route('/h_class/<int:h_class_id>')
def h_class(h_class_id):
    h_class = H_class.query.get(h_class_id)
    return render_template('h_class.html', title='H Class', h_class=h_class)

@bp.route('/l_classes')
def l_classes():
    l_classes = L_class.query.all()
    return render_template('l_classes.html', title='L classes', l_classes=l_classes)


@bp.route('/l_class/<int:l_class_id>')
def l_class(l_class_id):
    l_class = L_class.query.get(l_class_id)
    return render_template('l_class.html', title='L Class', l_class=l_class)


@bp.route('/r_classes')
def r_classes():
    r_classes = R_class.query.all()
    return render_template('r_classes.html', title='R classes', r_classes=r_classes)


@bp.route('/r_class/<int:r_class_id>')
def r_class(r_class_id):
    r_class = R_class.query.get(r_class_id)
    return render_template('r_class.html', title='R Class', r_class=r_class)


@bp.route('/d_class/<int:d_class_id>')
def d_class(d_class_id):
    d_class = D_class.query.get(d_class_id)
    return render_template('d_class.html', title='D Class', d_class=d_class)


@bp.route('/d_classes')
def d_classes():
    d_classes = D_class.query.all()
    return render_template('d_classes.html', title='D classes', d_classes=d_classes)
