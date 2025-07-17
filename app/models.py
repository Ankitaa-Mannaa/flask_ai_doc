from flask_mongoengine import MongoEngine
from datetime import datetime, timezone

db = MongoEngine()

class User(db.Document):
    name = db.StringField(max_length=150)
    email = db.StringField(max_length=150, unique=True)
    password_hash = db.StringField(max_length=150)
    role = db.StringField(max_length=50, default='user')

class Document(db.Document):
    filename = db.StringField(max_length=200)
    user = db.ReferenceField(User)
    upload_time = db.DateTimeField(default=lambda: datetime.now(timezone.utc))

class Chunk(db.Document):
    doc = db.ReferenceField(Document)
    text = db.StringField()
    embedding = db.ListField()  # store embedding vector as list

class Log(db.Document):
    user = db.ReferenceField(User)
    action = db.StringField(max_length=255)
    timestamp = db.DateTimeField(default=lambda: datetime.now(timezone.utc))
