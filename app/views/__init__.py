# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from .main_views import main_blueprint
from .topics_views import topic_blueprint
from .key_views import key_blueprint
from .api_views import api_blueprint
from .message_views import message_blueprint

def register_blueprints(csrf, app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(topic_blueprint)
    app.register_blueprint(key_blueprint)
    csrf.exempt(api_blueprint)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(message_blueprint)
