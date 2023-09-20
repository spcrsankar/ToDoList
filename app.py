from flask import Flask, session, render_template, request, redirect, url_for, jsonify, Response
from validation import signup_validation, login_validation
import hashlib
import mongodb_connection
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import base64


load_dotenv()


def create_app():
  app = Flask(__name__)
  app.secret_key = ' jsdnfkhvfhf83sfjv'

  app.client = MongoClient(os.getenv("Mongo_URI"))
  app.db = app.client.ToDoList

  # date formate for UI calender
  def reverse_format(date):
      date = "2023 " + date
      date_obj = datetime.strptime(date, "%Y %b %d")
      formatted_date = date_obj.strftime("%Y-%m-%d")
      return formatted_date

  #date formate for database
  def date_format(date):
    if date == "":
      current_date = datetime.now()
      date = current_date.strftime("%Y-%m-%d")
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%b %d")
    return formatted_date

  @app.errorhandler(404)
  def page_not_found(e):
    return render_template('404.html'), 404

  @app.route('/',methods=['GET','POST'])
  def login():
      if request.method == 'POST':
          #get all data from form
          email = request.form['email']
          password = request.form['password']
          
          #validate data
          msg = login_validation(email, password)
          
          #if valid
          if msg == "Ok":
            #check with database and update
            msg = mongodb_connection.login_validation_db(app.db,email, password)

            if msg[0] == "Ok":
              session['email'] = email
              session['username'] = msg[1]
              return redirect(url_for('home'))
            
          return render_template('login.html',msg=msg[0],email=email,password=password)
      return render_template('login.html')


  @app.route('/signup/', methods=['GET', 'POST'])
  def signup():
      if request.method == 'POST':
          print('post request',request.files)
          #get image and convert to base64
          if('profile' in request.files):
             print('file is there')
          else:
            print('file is not there')
          file = request.files['profile']

          print('file is collected')
          image_binary = file.read()
          image_base64 = base64.b64encode(image_binary).decode('utf-8')
          print('image is converted')
          
          #get all data
          user_name = request.form['username']
          password = request.form['password']
          email = request.form['email']
          
          #validate data 
          msg = signup_validation(user_name, password, email)
          
          #if valid
          if msg == "Ok":
            #check with database
            msg = mongodb_connection.insert_user(app.db,user_name, password, email, image_base64)

            if(msg == "Ok"):
              session['username'] = user_name
              session['email'] = email
              return redirect(url_for('login'))
              
          return render_template('signup.html',msg=msg,username=user_name,email=email,password=password,profile_image=image_base64)
      
      return render_template('signup.html',msg="")

  @app.route('/home/')
  def home():
      if 'username' in session:
        print(session['email'],session['username'])
        profile_image = mongodb_connection.get_profile_image(app.db,session['email'])

        #get tasks from database
        tasks = mongodb_connection.get_tasks(app.db,session['email'])  
        return render_template('home.html',username=session['username'],tasks=tasks)
      return redirect(url_for('login'))

  #to get current users profile image
  @app.route('/profile-image/')
  def profile_image():
    image_data = mongodb_connection.get_profile_image(app.db,session['email'])  

    if image_data:
        # Decode the base64-encoded image data
        image_base64 = image_data
        image_binary = base64.b64decode(image_base64)

        # Create a response with the image binary data
        response = Response(image_binary, content_type='image/jpeg')  # You can adjust the content type based on your image type

        return response

    else:
        return redirect(url_for('login'))

  @app.route('/logout/')
  def logout():
      
      session.pop('username', None)
      return redirect(url_for('login'))

  # update task status
  @app.route('/complete/<int:task_id>/')
  def complete(task_id):
      if 'username' in session:
        msg = mongodb_connection.complete_task(app.db,session['email'],task_id)
        return "OK", 200
      return "Not Found", 404

  # delete task
  @app.route('/delete/<int:task_id>/')
  def delete(task_id):
      if 'username' in session:
        msg = mongodb_connection.delete_task(app.db,session['email'],task_id)
        return "OK", 200
      return "Not Found", 404

  # add task
  @app.route('/add/', methods=['POST'])
  def add():
      if 'username' in session:
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        date = date_format(date)
        new_task = {
            'title': title,
            'description': description,
            'is_completed': False,
            'due_date': date
        }
        msg = mongodb_connection.add_task(app.db,session['email'],new_task)
        return redirect(url_for('home'))
      return redirect(url_for('login'))

  # search task based on title
  @app.route('/search/<string:search_text>/')
  def search(search_text):
      if 'username' in session:
        search_text = search_text.lower()
        search_result = []
        tasks = mongodb_connection.get_tasks(app.db,session['email'])
        
        for task in tasks:
          if search_text in task['title'].lower():
            search_result.append(task['id'])
        
        return jsonify(search_result)
    
      return redirect(url_for('login'))

  # get task details
  @app.route('/get_task/<int:task_id>/')
  def get_task(task_id):
      if 'username' in session:
        task = mongodb_connection.get_task(app.db,session['email'],task_id)
        temp = task.copy()
        temp['due_date'] = reverse_format(temp['due_date'])
            
        return jsonify(temp)
      return redirect(url_for('login'))

  # update task details
  @app.route('/update/<int:task_id>/', methods=['POST'])
  def update(task_id):
      if 'username' in session:
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        date = date_format(date)

        mongodb_connection.update_task(app.db,session['email'],task_id,{
            'id': task_id,
            'title': title,
            'description': description,
            'due_date': date
        })
        
        return redirect(url_for('home'))
      return redirect(url_for('login'))
  
  return app