

from flask import Flask, redirect, url_for

from evememorygame.settings   import DevConfig
from evememorygame.extensions import register_extensions
from evememorygame.modules    import register_apis


def create_app(config_object=DevConfig):
    """  application factory. """

    app = Flask(__name__)
    app.config.from_object(config_object)
    
    register_apis()
    register_extensions(app)

    return app