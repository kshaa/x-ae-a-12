from flask import Blueprint, redirect, render_template
from flask import request, url_for, current_app
from flask_user import current_user, login_required

from app import db
from app.models.message_models import Messages, MessageForm, Topic, Subscription
from app.models.user_models import User

from pywebpush import webpush
import json

import traceback
import logging

from sqlalchemy import join
from sqlalchemy.sql import select

message_blueprint = Blueprint('messages', __name__, template_folder='templates')

@message_blueprint.route('/topics/<topic_id>/messages/create', methods=['GET', 'POST'])
@login_required
def create_message_page(topic_id):
    # Initialize form
    message = Messages()
    form = MessageForm(request.form, obj=message)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(message)
        message.topic_id = topic_id
        # Add topic
        db.session.add(message)
        # Save topic
        db.session.commit()

        # Send notification
        subscriptions = Subscription.query.filter(Subscription.owner_user_id == current_user.id).all()
        for subscription in subscriptions:
            try:
                webpush(subscription_info = json.loads(subscription.subscription), data = message.content, vapid_private_key = current_app.config['SERVER_PRIVATE_NOTIFICATION_KEY'], vapid_claims = {"sub": "mailto:" + current_app.config['NOTIFICATION_SENDTO_EMAIL']})
            except Exception as e:
                logging.error(traceback.format_exc())

        # Redirect to listing
        return redirect(url_for('messages.view_messages_page', topic_id = topic_id))

    # Process GET or invalid POST
    return render_template('messages/messages_create.html', page_title = "Create message", form = form)

@message_blueprint.route('/topics/<topic_id>/messages', methods=['GET'])
@login_required
def view_messages_page(topic_id):
    topic = Topic.query.filter (Topic.id == topic_id).one()
    if topic.owner_user_id != current_user.id:
        return 'bad request!', 400
    messages = Messages.query.filter(Messages.topic_id == topic_id).limit(20).all()
    return render_template('messages/messages.html', topic_id = topic_id, page_title = "Topic messages", messages = messages, topic = topic)
