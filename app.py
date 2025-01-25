from flask import Flask , render_template , request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)  


#configuraton de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#création de la table taches
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Task : {self.id}: {self.task} {self.completed}'



@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        new_task = request.form['task']
        if new_task:
            task = Task(task=new_task)
            db.session.add(task)
            db.session.commit()
    tasks = Task.query.all()




    #gestion des recherche et filtrage des taches
    search = request.args.get('search', "")
    filtrage = request.args.get('filter', 'all')
    if filtrage == 'completed':
        tasks = Task.query.filter_by(completed=True).all()
    elif filtrage == 'not_completed':
        tasks = Task.query.filter_by(completed=False).all()
    else:
        tasks = Task.query.all()
    return  render_template('home.html', tasks = tasks)


    



@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')



@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)

