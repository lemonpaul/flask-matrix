from app import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/explore')
def explore():
    return render_template('explore.html', title='Theory')