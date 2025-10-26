from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)


# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# In-memory "database"
tasks = []

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='To Do')  # To Do, In Progress, Done
    priority = db.Column(db.String(10), default='Medium')  # Low, Medium, High

    def __repr__(self):
        return f'<Task {self.title}>'

# READ
with app.app_context():
    db.create_all()
@app.route('/')
def index():
    tasks = Task.query.all()  # Get all tasks from the database
    return render_template('index.html', tasks=tasks)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        priority = request.form.get('priority', 'Medium')

        new_task = Task(title=title, description=description, priority=priority)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))

    # If it's a GET request, just render the form
    return render_template('create.html')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)  # Find the task by ID
    db.session.delete(task)         # Remove it
    db.session.commit()             # Save changes
    return redirect(url_for('index'))

# Update an existing task
@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form.get('description', '')
        task.status = request.form.get('status', task.status)
        task.priority = request.form.get('priority', task.priority)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update.html', task=task)



# # CREATE
# @app.route('/create', methods=['GET', 'POST'])
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         tasks.append({'id': len(tasks) + 1, 'title': title})
#         return redirect(url_for('index'))
#     return render_template('create.html')
#
#
# # UPDATE
# @app.route('/update/<int:task_id>', methods=['GET', 'POST'])
# def update(task_id):
#     task = next((t for t in tasks if t['id'] == task_id), None)
#     if request.method == 'POST':
#         task['title'] = request.form['title']
#         return redirect(url_for('index'))
#     return render_template('update.html', task=task)
#
#
# # DELETE
# @app.route('/delete/<int:task_id>')
# def delete(task_id):
#     global tasks
#     tasks = [t for t in tasks if t['id'] != task_id]
#     return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
