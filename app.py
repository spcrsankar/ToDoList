from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from validation import signup_validation, login_validation

from datetime import datetime

app = Flask(__name__)
app.secret_key = ' jsdnfkhvfhf83sfjv'


def date_format(date):
  print(date+"date")
  if date == "":
    current_date = datetime.now()
    date = current_date.strftime("%Y-%m-%d")
  date_obj = datetime.strptime(date, "%Y-%m-%d")
  formatted_date = date_obj.strftime("%b %d")
  return formatted_date

user = {
    'username': 'sankar',
    'no_of_tasks': 4,   #to keep track of task it
}
tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
        'is_completed': True,
        'due_date': 'Oct 20'

    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web',
        'is_completed': True,
        'due_date': 'Oct 20'

    },
    {
        'id': 3,
        'title': 'Learn Flask',
        'description': 'Need to find a good Flask tutorial on the web',
        'is_completed': False,
        'due_date': 'Oct 20'
    
    },
    {
        'id': 4,
        'title': 'Learn Django',
        'description': 'Need to find a good Django tutorial on the web',
        'is_completed': False,
        'due_date': 'Oct 20'
    }
]

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #get all data
        email = request.form['email']
        password = request.form['password']
        
        #validate data
        msg = login_validation(email, password)
        
        #if valid
        if msg == "Ok":
          #update database
          session['email'] = email
          session['username'] = user['username']
          return redirect(url_for('home'))
        return render_template('login.html',msg=msg,email=email,password=password)
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #get all data
        user_name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        #validate data
        msg = signup_validation(user_name, password, email)
        
        #if valid
        if msg == "Ok":
          #update database

          return redirect(url_for('login'))
        return render_template('signup.html',msg=msg,username=user_name,email=email,password=password)
    
    return render_template('signup.html',msg="")

@app.route('/home/')
def home():
    #get data from database
    print(session)
    if 'username' in session:
        return render_template('home.html',username=session['username'],tasks=tasks)
    return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/complete/<int:task_id>/')
def complete(task_id):
    print('complete')
    if 'username' in session:
      for task in tasks:
          if task['id'] == task_id:
              task['is_completed'] = not task['is_completed']
      print(tasks)
      return "OK", 200
    return "Not Found", 404

@app.route('/delete/<int:task_id>/')
def delete(task_id):
    print('delete')
    if 'username' in session:
      for task in tasks:
          if task['id'] == task_id:
              tasks.remove(task)
      print(tasks)
      return "OK", 200
    return "Not Found", 404

@app.route('/add/', methods=['POST'])
def add():
    print('add')
    if 'username' in session:
      title = request.form['title']
      description = request.form['description']
      date = request.form['date']
      date = date_format(date)
      print(title, description)
      user['no_of_tasks'] += 1
      tasks.append({
          'id': user['no_of_tasks'],
          'title': title,
          'description': description,
          'is_completed': False,
          'due_date': date
      })
      print(tasks)
      return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/search/<string:search_text>/')
def search(search_text):
   if 'username' in session:
      print(search_text)
      search_text = search_text.lower()
      search_result = []
      for task in tasks:
        if search_text in task['title'].lower():
          search_result.append(task['id'])
      print(search_result)
      return jsonify(search_result)