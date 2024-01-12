from app import app, db
from models import Hero, Power, Hero_Power



#powers
powers =[
    {'name': "super strength", 'description': "gives the wielder super-human strengths"},
    {'name': "flight", 'description': "gives the wielder the ability to fly through the skies at supersonic speed"},
    {'name': "super human senses", 'description': "allows the wielder to use her senses at a super-human level"},
    {'name': "elasticity", 'description': "can stretch the human body to extreme lengths"}
]

#instances
for power_data in powers:
    power = Power(**power_data)  
    db.session.add(power)




#hero
heroes =[
    {'name': "Kamala Khan", 'super_name': "Ms. Marvel"},
    {'name': "Doreen Green", 'super_name': "Squirrel Girl"},
    {'name': "Gwen Stacy", 'super_name': "Spider-Gwen"},
    {'name': "Janet Van Dyne", 'super_name': "The Wasp"},
    {'name': "Wanda Maximoff", 'super_name': "Scarlet Witch"},
    {'name': "Carol Danvers", 'super_name': "Captain Marvel"},
    {'name': "Jean Grey", 'super_name': "Dark Phoenix"},
    {'name': "Ororo Munroe", 'super_name': "Storm"},
    {'name': "Kitty Pryde", 'super_name': "Shadowcat"},
    {'name': "Elektra Natchios", 'super_name': "Elektra"}
]
#instances for hero
for hero_data in heroes:
    hero = Hero(**hero_data)
    db.session.add(hero)



#add powers to hero
strengths = ["Strong", "Weak", "Average"]
# Add powers to heroes
for hero in heroes:
    for _ in range(1, 4):  # Assign 1-3 powers to each hero
        power = Power.query.order_by(db.func.random()).first()
        hero_power = Hero_Power(hero=hero, power=power, strength="Strong")
        db.session.add(hero_power)

db.session.commit()

#  Done seeding!")
print("YOU ARE SO COOL, MADE IT TO THE END!!!!!")

'''if __name__ == '__main__':
    app.context()
    print("YOU ARE SO COOL, MADE IT TO THE END!!!!!")'''
