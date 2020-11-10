from app.main import bp
from app.models import Matrix
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
    next_url = url_for('main.matrices', page=matrices.next_num) \
        if matrices.has_next else None
    prev_url = url_for('main.matrices', page=matrices.prev_num) \
        if matrices.has_prev else None
    return render_template('matrices.html', title='Matrices', matrices=matrices.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/classes')
def classes():
    matrices = Matrix.query.all()[-136:-120]
    return render_template('classes.html', title='Classes', matrices=matrices)

