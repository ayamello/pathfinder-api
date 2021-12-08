from flask import Flask
from app.routes.api_blueprint import bp as bp_api

def init_app(app: Flask):
    app.register_blueprint(bp_api)

