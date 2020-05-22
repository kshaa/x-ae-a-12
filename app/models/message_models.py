from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db
from secrets import token_hex

# Define the API Keys data model
class APIKeys(db.Model):
    __tablename__ = 'apikeys'
    id = db.Column(db.Integer(), primary_key=True)
    owner_user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    key = db.Column(db.String(512), nullable=False, unique=True)
    label = db.Column(db.String(512), nullable=True)

    def __init__(self):
        self.key = token_hex(256) 

# Define the User profile form
class APIKeyCreateForm(FlaskForm):
    label = StringField('Label', validators=[
        validators.DataRequired('Label is required')])
    submit = SubmitField('Create API key')

# Define the Topic data model
class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer(), primary_key=True)
    owner_user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    code = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'') # for display purposes

# Define the Messages data model
class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer(), primary_key=True)
    topic_id = db.Column(db.Integer(), db.ForeignKey('topics.id', ondelete='CASCADE'))
    content = db.Column(db.Unicode(255), server_default=u'') # for display purposes

# Define the Topics form
class TopicsForm(FlaskForm):
    code = StringField('Code', validators=[
        validators.DataRequired('Topic code is required')])
    label = StringField('Label', validators=[
        validators.DataRequired('Topic label is required')])
    submit = SubmitField('Create topic')

# Define the Topics form
class MessageForm(FlaskForm):
    content = StringField('Content', validators=[
        validators.DataRequired('Content is required')])
    submit = SubmitField('Create message')
