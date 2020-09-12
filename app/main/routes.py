from app.main import bp
from flask import render_template


@bp.route('/')
def index():
    return render_template('index.html', title='Home')

@bp.route('/explore')
def explore():
    return render_template('explore.html', title='Theory')