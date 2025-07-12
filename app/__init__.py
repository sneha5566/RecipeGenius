from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipegenius.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ CORRECT WAY to import and register auth blueprint
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.recipe import bp as recipe_bp
    app.register_blueprint(recipe_bp)

    from app.routes.search import search_bp
    app.register_blueprint(search_bp)

    from app.routes.saved import saved_bp
    app.register_blueprint(saved_bp, url_prefix='/saved')

    from app.routes.meal_planner import planner_bp
    app.register_blueprint(planner_bp)

    from app.routes.shopping_list import shopping_bp
    app.register_blueprint(shopping_bp)

    from app.routes.meal import meal_bp
    app.register_blueprint(meal_bp)

    from app.routes.nutrition import nutrition_bp
    app.register_blueprint(nutrition_bp)


    



    @app.route('/')
    def home():
        username = session.get('username')
        
        return render_template('home.html', username=username)

    app.add_url_rule('/', endpoint='home', view_func=home)
    return app
