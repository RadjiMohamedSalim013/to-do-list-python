from flask import Flask , render_template , request, redirect, url_for

app = Flask(__name__)  


# listes des taches
tasks = ['task1','task2','task3','task4','task5']



@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        new_task = request.form['task']
        if new_task:
            tasks.append(new_task)
    return  render_template('home.html', tasks = tasks)


#supression d'une taches
@app.route('/delete', methods=['POST'])
def delete_task():
    task_delete = request.form.get('task_delete')
    tasks.remove(task_delete)
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)

