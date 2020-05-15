from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db

# Define the API Keys data model
class APIKeys(db.Model):
    __tablename__ = 'apikeys'
    id = db.Column(db.Integer(), primary_key=True)
    owner_user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    key = db.Column(db.String(255), nullable=False, server_default=u'', unique=True)

# Define the Topic data model
class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer(), primary_key=True)
    owner_user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'') # for display purposes

# Define the Messages data model
class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer(), primary_key=True)
    topic_id = db.Column(db.Integer(), db.ForeignKey('topics.id', ondelete='CASCADE'))
    content = db.Column(db.Unicode(255), server_default=u'') # for display purposes