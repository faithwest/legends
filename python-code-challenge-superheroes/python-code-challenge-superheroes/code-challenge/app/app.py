#!/usr/bin/env python3
#RESTFul imports
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Hero ,Power ,Hero_Power


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

#Home index
@app.route('/')
def home():
    return '({Get Ready To Exlpore!!})'

#heroes

#get all
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()#get all heroes
    #converted to JSON and returned the response
    result = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(result)

#retrieve specific hero id,otherwise return an error
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)#get the specified id
    if hero:
        result = {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': []}
        for hero_power in HeroPower.query.filter_by(hero_id=id).all():
            power = Power.query.get(hero_power.power_id)#its power and the result converted to json
            result['powers'].append({
                'id': power.id,
                'name': power.name,
                'description': power.description
            })
        return jsonify(result)
    else:
        return jsonify({"error": "Hero not found"}), 404

#powers

#get powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()#retrieve all powers from db
    #creates a list of id ,name and description(result)
    result = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(result)#returns results in json

#retrieve specific id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        #to return dictionary if found
        result = {'id': power.id, 'name': power.name, 'description': power.description}
        return jsonify(result)#convert to json
    else:
        return jsonify({"error": "Power not found"}), 404

#update a specified power id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)#get specified id
    if power:
        try:
            data = request.get_json()
            power.description = data['description']
            db.session.commit()#commit the changes to db
            #dictionary result if found
            result = {'id': power.id, 'name': power.name, 'description': power.description}
            return jsonify(result)#convert to json
        except KeyError:
            return jsonify({"errors": ["validation errors"]}), 400
    else:
        #otherwise if not found,throw a 404 error
        return jsonify({"error": "Power not found"}), 404


#new relationship between hero and power
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.get_json()
        hero_id = data['hero_id']
        power_id = data['power_id']
        strength = data['strength']
        
        #  do hero and power exist
        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)
        
        #if they dont exist,return an error
        if not hero or not power:
            return jsonify({"error": "Hero or Power not found"}), 404

        # make a new HeroPower relations
        hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=strength)
        db.session.add(hero_power)
        db.session.commit()#commit the changes

        # get hero's with their powers
        result = {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': []}
        for hero_power in HeroPower.query.filter_by(hero_id=hero.id).all():
            power = Power.query.get(hero_power.power_id)
            result['powers'].append({
                'id': power.id,
                'name': power.name,
                'description': power.description
            })
        
        return jsonify(result)#convert it to json
    
    except KeyError:
        return jsonify({"errors": ["validation errors"]}), 400        


if __name__ == '__main__':
    app.run(port=4600, debug=True)
