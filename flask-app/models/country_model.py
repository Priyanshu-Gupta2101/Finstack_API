from database import db
from datetime import datetime, timezone

class Country(db.Model):
    """Country model for multi-country support"""
    __tablename__ = 'countries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(3), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    farmer = db.relationship('Farmer', back_populates='country')
    
    def __repr__(self):
        return f'<Country {self.name}>'
