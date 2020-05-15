from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required

from app import db
from app.models.message_models import APIKeys, APIKeyCreateForm

from pprint import pprint

key_blueprint = Blueprint('keys', __name__, template_folder='templates')

# The User page is accessible to authenticated users (users that have logged in)
@key_blueprint.route('/keys')
@login_required
def list_keys():
    keys = APIKeys.query.all()
    return render_template('keys/list_keys.html', keys=keys)

@key_blueprint.route('/keys/create', methods=['GET', 'POST'])
@login_required
def create_key():
    key = APIKeys()
    form = APIKeyCreateForm(request.form, obj=key)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Create API key
        key.owner_user_id = current_user.id

        # Save API key
        db.session.add(key)
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('keys.list_keys'))

    # Process GET or invalid POST
    return render_template('keys/create_key.html', form=form)
