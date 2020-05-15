# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from .main_views import key_blueprint
from .topics_views import topic_blueprint

def register_blueprints(app):
    app.register_blueprint(key_blueprint)
    app.register_blueprint(topic_blueprint)