from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    low_threshold = db.Column(db.Float, default=0.0)
    high_threshold = db.Column(db.Float, default=1000.0)

    def __repr__(self):
        return f'<User {self.username}>'
