from database import db
from datetime import datetime, timezone

class Farm(db.Model):
    """Farm model with area, village, crop, sowing date"""
    __tablename__ = 'farms'
    
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Numeric(10, 2), nullable=False)  # in Acres
    village = db.Column(db.String(100), nullable=False)
    crop_grown = db.Column(db.String(100), nullable=False)
    sowing_date = db.Column(db.Date, nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    schedule = db.relationship('Schedule', back_populates='farm', cascade='all, delete-orphan')
    farmer = db.relationship('Farmer', back_populates='farm')
    
    def __repr__(self):
        return f'<Farm {self.crop_grown} - {self.village}>'