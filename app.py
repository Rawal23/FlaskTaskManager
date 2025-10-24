from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory "database"
tasks = []


# READ
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)


# CREATE
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        tasks.append({'id': len(tasks) + 1, 'title': title})
        return redirect(url_for('index'))
    return render_template('create.html')


# UPDATE
@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if request.method == 'POST':
        task['title'] = request.form['title']
        return redirect(url_for('index'))
    return render_template('update.html', task=task)


# DELETE
@app.route('/delete/<int:task_id>')
def delete(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
