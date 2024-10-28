from flask import Flask,render_template
from flask_bootstrap import Bootstrap as Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # enable bootstrap utility
    Bootstrap5(app)

    # initialise session object
    app.secret_key = 'somerandomvalue'

    # Configue and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///websitedb.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id==user_id))
    
    #add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import events
    app.register_blueprint(events.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    #error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html", error=e), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("500.html", error=e), 500
    
    @app.route('/trigger-500')
    def trigger_error():
    # This will raise a 500 error
        return 1 / 0  # Deliberate error to test the 500 handler

    return app