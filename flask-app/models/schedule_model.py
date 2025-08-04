from database import db
from datetime import datetime, timezone

class Schedule(db.Model):
    """Schedule model with days after sowing, fertilizer, quantity"""
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    days_after_sowing = db.Column(db.Integer, nullable=False)
    fertilizer = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Numeric(10, 3), nullable=False)
    quantity_unit = db.Column(db.String(10), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    farm = db.relationship('Farm', back_populates='schedule')
    
    def __repr__(self):
        return f'<Schedule {self.fertilizer} - Day {self.days_after_sowing}>'
