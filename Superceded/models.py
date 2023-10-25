from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  
from datetime import timedelta  
#from flask_user import UserMixin, UserManager

db = SQLAlchemy()

class League(db.Model):
    __tablename__ = 'League'
    id = db.Column(db.Integer, primary_key=True)
    league_name = db.Column(db.String(40), nullable=False)

class User(db.Model):
    __tablename__ = 'User'  # Replace with the actual table name in your database
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    username = db.Column(db.String(25), unique=True, nullable=False)
    user_password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Integer, nullable=False)

class NewsAnnouncements(db.Model):
    __tablename__ = 'News_Announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publish_date = db.Column(db.Date, nullable=False)

class ChatMessage(db.Model):
    __tablename__ = 'Chat_Message'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    chat_timestamp = db.Column(db.DateTime, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)

# user_manager = UserManager(None, db, User)