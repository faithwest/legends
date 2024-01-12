from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates



db = SQLAlchemy()


#HERO
class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    super_name = db.Column(db.String(80))
    powers = db.relationship('Power', secondary='hero_power', backref='heroes_with_power', lazy='dynamic')


#POWER
class Power(db.Model):
    __tablename__ = "power"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255)) 
    heroes= db.relationship('Hero', backref='powers_for_hero', secondary='hero_power', lazy='dynamic')

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
    hero = db.relationship('Hero', backref='powers')
    power = db.relationship('Power', backref='heroes')

    @validates('strength')
    def validate_strength(self, key, strength):
        assert strength in ['Strong', 'Weak', 'Average'], f"Invalid strength: {strength}"
        return strength

