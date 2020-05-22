# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Response, Blueprint, redirect, render_template
from flask import request, url_for, send_from_directory
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.message_models import Subscription
from app.models.user_models import UserProfileForm, NotificationSubscriptionForm, NotificationUnsubscriptionForm

main_blueprint = Blueprint('main', __name__, static_folder='static', template_folder='templates')

# Push notification service worker must be at root
@main_blueprint.route('/sw.js')
def service_worker():
    return send_from_directory('static/scripts', 'sw.js')

@main_blueprint.route('/subscribe', methods=['POST'])
@login_required
def subscribe():
    form = NotificationSubscriptionForm(request.form)

    # Process valid POST
    if form.validate():
        subscription = Subscription.query.\
            filter(Subscription.owner_user_id == current_user.id).\
            filter(Subscription.subscription == form.subscription.data).\
            first()

        if not subscription:
            subscription = Subscription()
            subscription.subscription = form.subscription.data
            subscription.owner_user_id = current_user.id
            db.session.add(subscription)
            db.session.commit()

        return Response("{ success: true }", mimetype='application/json')
    else:
        return "{ success: false }"

@main_blueprint.route('/unsubscribe', methods=['POST'])
@login_required
def unsubscribe():
    form = NotificationUnsubscriptionForm(request.form)

    # Process valid POST
    if form.validate():
        subscription = Subscription.query.\
            filter(Subscription.owner_user_id == current_user.id).\
            delete()
        db.session.commit()

        return Response("{ success: true }", mimetype='application/json')
    else:
        return "{ success: false }"

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return render_template('main/home_page.html')

@main_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/profile.html', page_title="User profile", form=form)

