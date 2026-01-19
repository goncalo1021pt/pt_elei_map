from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class DicoCode(db.Model):
    """DICO geographical codes (Districts, Concelhos, Freguesias)"""
    __tablename__ = 'dico_codes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6), unique=True, nullable=False, index=True)
    level = db.Column(db.Integer, nullable=False, index=True)  # 1=District, 2=Concelho, 3=Freguesia
    name = db.Column(db.String(255), nullable=False)
    parent_code = db.Column(db.String(6), db.ForeignKey('dico_codes.code'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    children = db.relationship('DicoCode', remote_side=[code], backref='parent')
    results = db.relationship('Result', backref='location', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<DicoCode {self.code} - {self.name}>'

    def to_dict(self):
        return {
            'code': self.code,
            'level': self.level,
            'name': self.name,
            'parent_code': self.parent_code
        }


class Election(db.Model):
    """Election metadata"""
    __tablename__ = 'elections'

    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(50))  # e.g., 'presidential', 'legislative', 'european'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    results = db.relationship('Result', backref='election', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Election {self.election_id} - {self.name}>'

    def to_dict(self):
        return {
            'election_id': self.election_id,
            'name': self.name,
            'date': self.date.isoformat(),
            'type': self.type
        }


class Result(db.Model):
    """Election results by geography and party"""
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.String(50), db.ForeignKey('elections.election_id'), nullable=False, index=True)
    dico_code = db.Column(db.String(6), db.ForeignKey('dico_codes.code'), nullable=False, index=True)
    party_code = db.Column(db.String(10), nullable=False)
    votes = db.Column(db.Integer, default=0)
    percentage = db.Column(db.Numeric(5, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Unique constraint to prevent duplicates
    __table_args__ = (
        db.UniqueConstraint('election_id', 'dico_code', 'party_code', name='uq_result'),
    )

    def __repr__(self):
        return f'<Result {self.election_id}/{self.dico_code}/{self.party_code}>'

    def to_dict(self):
        return {
            'election_id': self.election_id,
            'dico_code': self.dico_code,
            'party_code': self.party_code,
            'votes': self.votes,
            'percentage': float(self.percentage) if self.percentage else None
        }
