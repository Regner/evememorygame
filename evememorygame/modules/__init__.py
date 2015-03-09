

from evememorygame.extensions import api

def register_apis():
    from evememorygame.modules.questions.api import register_apis
    register_apis(api)
    