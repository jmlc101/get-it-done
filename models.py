from app import db

class Task(db.Model):

    # gives each task object unique integer
    id = db.Column(db.Integer, primary_key=True)
    # represents the name of task that is created, 
    # String data types, need to set maximum lenght ie: 120:
    name = db.Column(db.String(120))

    #boolean that will indicate if task completed
    completed = db.Column(db.Boolean)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, owner):
        self.name = name
        self.completed = False
        self.owner = owner



class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True) #when sql creates table for user, no 2 different records with same email. "unique"
    password = db.Column(db.String(120))
    
    tasks = db.relationship('Task', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password
