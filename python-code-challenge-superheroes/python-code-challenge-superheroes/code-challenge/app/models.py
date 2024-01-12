from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates



db = SQLAlchemy()


#HERO
class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    power = db.Column(db.String(100))
    power = db.relationship('Power', secondary='hero_power', backref='heroes', lazy='dynamic')


#POWER
class Power(db.Model):
    __tablename__ = "power"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255)) 
    hero= db.relationship('Hero', backref='hero_power', secondary='hero', lazy='dynamic')

    @validates('description')
    def validate_description(self, key, description):
        assert description and len(description) >= 20, "Description must be present and equal or more than 20 characters"
        return description

#HEROPOWER
class Hero_Power(db.Model):
    __tablename__ = "hero_power"

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'))
    strength = db.Column(db.String(20))
    hero = db.relationship('Hero', backref=db.backref('power', lazy='dynamic'))
    power = db.relationship('Power', backref=db.backref('heroe', lazy='dynamic'))

    @validates('strength')
    def validate_strength(self, key, strength):
        assert strength in ['Strong', 'Weak', 'Average'], f"Invalid strength: {strength}"
        return strength

