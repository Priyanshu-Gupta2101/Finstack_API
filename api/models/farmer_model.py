from database import db
from datetime import datetime, timezone

class Farmer(db.Model):
    """Farmer model with phone, name, language per country"""
    __tablename__ = 'farmers'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    farms = db.relationship('Farm', backref='farmer', cascade='all, delete-orphan')
    
    __table_args__ = (db.UniqueConstraint('phone_number', 'country_id', name='unique_phone_per_country'),)
    
    def __repr__(self):
        return f'<Farmer {self.name}>'