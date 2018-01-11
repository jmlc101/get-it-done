from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Task(db.Model):

    # gives each task object unique integer
    id = db.Column(db.Integer, primary_key=True)
    # represents the name of task that is created, 
    # String data types, need to set maximum lenght ie: 120:
    name = db.Column(db.String(120))

    #boolean that will indicate if task completed
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True) #when sql creates table for user, no 2 different records with same email. "unique"
    password = db.Column(db.String(120))
    
    def __init__(self, email, password):
        self.email = email
        self.password = password


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()

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

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/login")
def login():
    return render_template('login.html')



# To run from python shell
# sheild app.run call with:
if __name__ == '__main__':
    app.run()
    # sheilds any code w/i this conditional 
    # any code w/i conditional
    # ony runs if....or prevents start up ifff
    # ....bo back over....: