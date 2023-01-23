from app import app 
from models import db, connect_db, Pet 

db.drop_all() 
db.create_all() 

rambo = Pet(name='Rambo', species='German Shepperd')

db.session.add(rambo) 
db.session.commit()