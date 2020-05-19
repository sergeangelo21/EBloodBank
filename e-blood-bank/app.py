from flask import Flask
from config import Config

from blueprints.backend.backend import backend
from blueprints.backend.admin_hospital import admin_hospital
from blueprints.frontend.login import login
from blueprints.frontend.onevents import onevents
from blueprints.frontend.users import users

from os.path import join, isfile
from extensions import flask_login, db

def create_app():

	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(Config)
	app.register_blueprint(backend)
	app.register_blueprint(admin_hospital)
	app.register_blueprint(login)
	app.register_blueprint(onevents)
	app.register_blueprint(users)
	
	extensions(app)

	return app

def extensions(app):
    db.init_app(app)
    flask_login.init_app(app)

    return None

create_app().run(port=8000, debug=1)