from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from auth.routes import auth_bp
    from users.routes import users_bp
    from discussions.routes import discussions_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(discussions_bp, url_prefix='/discussions')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)