import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))

# init extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
# login_manager.login_message_category = "info"
bootstrap = Bootstrap5()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "my_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"

    # init extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    # bp for the index
    from .controllers.index import bp
    app.register_blueprint(bp, url_prefix=f"/")

    # bp for authentication routes
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # others bp
    from .controllers import blueprints
    for bp in blueprints():
        print(bp, bp.name)
        app.register_blueprint(bp, url_prefix=f"/{bp.name}")

    # login manager
    from .models import Aluno, Professor

    @login_manager.user_loader
    def load_user(user_id):
        print(f"the user id is: {user_id}")
        return Aluno.query.get(int(user_id)) or Professor.query.get(int(user_id))
        # return Aluno.query.filter_by(matricula=int(user_matricula)).first() or Professor.query.filter_by(matricula=int(user_matricula)).first()

    # initialize commands
    from .cli_commands import seed_cli
    app.cli.add_command(seed_cli)

    # thread initializer
    from .utils.th_check_aula_status import verificar_status_aulas
    import threading

    status_thread = threading.Thread(target=verificar_status_aulas, args=[app])
    status_thread.daemon = True
    status_thread.start()

    return app


app = create_app()
