from flask import Flask , render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='username',pw='password',url='127.0.0.1:5432',db='database name')

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)


from datetime import datetime


class Task(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/", methods = ['GET', 'POST'])
def index():

    if request.method == 'POST':
        task_content = request.form['content']
        if task_content == '':
            return "Task can't be added"
        new_task = Task(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return 'There was a problem adding your task'

    else:
        tasks = Task.query.order_by(Task.date_created.desc()).all()
        return render_template('index.html', tasks = tasks)


@app.route("/delete/<int:id>")
def delete_task(id):

    task = Task.query.get_or_404(id)
    if task:
        try:
            db.session.delete(task)
            db.session.commit()
            return redirect("/")

        except:
            return "There was problem"


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update_task(id):
    task = Task.query.get_or_404(id)
  
    if request.method == 'POST':
        task_content = request.form['content']
        if task_content == '':
            return redirect("/")
        task.content = request.form['content']
    
        try:
            db.session.commit()
            return redirect("/")
            
        except:
            return "There was problem"

    else:
        return render_template("update.html", task=task)

   
            
if __name__ == "__main__":
    app.run(debug=True)
