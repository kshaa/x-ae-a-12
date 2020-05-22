from flask import Blueprint, redirect, render_template, current_app
from flask import request, url_for, jsonify, make_response
from flask_user import current_user, login_required

from app import db
from app.models.user_models import User
from app.models.message_models import APIKeys, Topic, Messages

from pywebpush import webpush
import json

api_blueprint = Blueprint('api', __name__)

def response(status_code, success, message):
    payload = dict(
        success = success,
        message = message
    )

    return make_response(jsonify(payload), status_code)

@api_blueprint.route('/api/notify', methods=['GET'])
def notify():
    # Input
    api_key_value = request.args.get('api_key')
    topic_id = request.args.get('topic_id')
    topic_code = request.args.get('topic_code')
    message_content = request.args.get('message')

    # Validations    
    if not api_key_value:
        return response(400, False, "api_key not defined")
    if not topic_id and not topic_code:
        return response(400, False, "neither topic_id nor topic_code is defined")
    if topic_id and topic_code:
        return response(400, False, "only one of topic_id or topic_code must be defined")
    if not message_content:
        return response(400, False, "message not defined")

    # Search database for API key and topic
    api_key = APIKeys.query.filter(APIKeys.key == api_key_value).one()
    if not api_key:
        return response(400, False, "api_key not found")

    if topic_id:
        topic = Topic.query.filter(Topic.id == topic_id).one()
    else:
        topic = Topic.query.filter(Topic.code == topic_code).one()

    if not topic:
        return response(400, False, "topic not found")

    # Validate APIKey can access the given topic
    if topic.owner_user_id != api_key.owner_user_id:
        return response(400, False, "api_key has no access to the given topic")

    # Create new message
    message = Messages()
    message.owner_user_id = api_key.owner_user_id
    message.content = message_content

    # Store new message
    user = User.query.filter(User.id == api_key.owner_user_id).one()
    if not user:
        return response(400, False, "user doesn't exist anymore")

    db.session.add(message)
    db.session.commit()

    # Notify owner
    webpush(subscription_info = json.loads(user.subscription), data = message.content, vapid_private_key = current_app.config['SERVER_PRIVATE_NOTIFICATION_KEY'], vapid_claims = {"sub": "mailto:" + current_app.config['NOTIFICATION_SENDTO_EMAIL']})

    return response(200, True, "Successfully sent message to user")
