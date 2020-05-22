from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required

from app import db
from app.models.message_models import TopicsForm, Topic

topic_blueprint = Blueprint('topics', __name__, template_folder='templates')

@topic_blueprint.route('/topics/create', methods=['GET', 'POST'])
@login_required
def topics_page():
    # Initialize form
    topic = Topic()
    form = TopicsForm(request.form, obj=topic)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(topic)
        topic.owner_user_id = current_user.id
        # Add topic
        db.session.add(topic)
        # Save topic
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('topics.view_topics_page'))

    # Process GET or invalid POST
    return render_template('topics/topics_create.html',
                           form=form)

@topic_blueprint.route('/topics', methods=['GET'])
@login_required
def view_topics_page():
    topics = Topic.query.filter(Topic.owner_user_id == current_user.id).all()
    return render_template('topics/topics.html', page_title = "Message topics", topics = topics)
