from app import db
from datetime import datetime
from sqlalchemy import Text, JSON

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Optional personal information
    name = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    
    # Symptoms and diagnosis
    symptoms_selected = db.Column(JSON, nullable=False)  # List of selected symptoms
    symptoms_text = db.Column(Text, nullable=True)  # Free-text symptoms
    diagnosis = db.Column(JSON, nullable=False)  # Diagnosis results
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to feedback
    feedback = db.relationship('Feedback', backref='submission', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Submission {self.id}>'

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)
    
    # Feedback data
    is_accurate = db.Column(db.Boolean, nullable=False)
    comments = db.Column(Text, nullable=True)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Feedback {self.id} for Submission {self.submission_id}>'
