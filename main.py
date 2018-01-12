from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'asdfjklasdfjkl'


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


@app.route('/', methods=['POST', 'GET'])
def index():

    owner = User.query.filter_by(email=session['email']).first()# I did User.id.....no good

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name, owner)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False,owner=owner).all()
    completed_tasks = Task.query.filter_by(completed=True,owner=owner).all()

    return render_template('todos.html',title="Get It Done!", 
        tasks=tasks, completed_tasks=completed_tasks)

@app.route("/delete-task", methods=["POST"])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - VALIDATE USER DATA ON YOUR OWN
        #if data valid, create User

        existing_user = User.query.filter_by(email=email).first() #query syntax? if user exist, will assign vaule otherwise will assign 'NONE'.
        if not existing_user: #if not existing user, create user.
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('register.html')

#so no flask handler, we want this to run for every request 
@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #now need to verify password
        user = User.query.filter_by(email=email).first() #query syntax? if user exist, will assign vaule otherwise will assign 'NONE'.
        if user and user.password == password: #checks if user exists and if password == password
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')



# To run from python shell
# sheild app.run call with:
if __name__ == '__main__':
    app.run()
    # sheilds any code w/i this conditional 
    # any code w/i conditional
    # ony runs if....or prevents start up ifff
    # ....bo back over....: