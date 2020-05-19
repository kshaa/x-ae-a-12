from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required

from app import db

api_blueprint = Blueprint('api', __name__)

# @api_blueprint.route('/api/subscribe', methods=['POST'])
# @login_required
# def subscribe():
#     # print('Subscribed' + current_user.id)
#     return 'Ok'

# @api_blueprint.route('/api/unsubscribe', methods=['POST'])
# # @login_required
# # @csrf.exempt
# def unsubscribe():
#     # print('Unsubscribed' + current_user.id)
#     return 'Ok'
