import click
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    @app.cli.command('init')
    @click.option('--height', default=3, help='Maximum matix height.')
    @click.option('--width', default=3, help='Maximum matrix width.')
    def init(height, width):
        """ Initialize matrices and classes """
        from app.tasks import init
        init(int(height), int(width))

    return app
