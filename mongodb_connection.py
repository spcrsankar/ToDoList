import hashlib

def check_user_exists(db, email):
    user = db.users.find_one({'email': email})
    if user:
        return True
    return False

def insert_user(db,user_name, password, email, image_base64):
    if check_user_exists(db, email):
        return "Email already registered"
    print('mongodb_connection.py')
    print('insert_user')
    print(user_name, password, email)
    password = hashlib.sha256(password.encode()).hexdigest()
    db.users.insert_one({
        "username": user_name,
        "password": password,
        "email": email,
        'profile_image': image_base64,
        "no_of_tasks": 0,
        "tasks": []
    })
    return "Ok"

def login_validation_db(db, email, password):
    if not check_user_exists(db, email):
        return "Email not registered",None
    password = hashlib.sha256(password.encode()).hexdigest()
    user = db.users.find_one({'email': email})
    if user['password'] == password:
        return "Ok",user['username']
    return "Incorrect password", None

def get_tasks(db,email):
    user = db.users.find_one({'email': email})
    return user.get('tasks', [])

def get_task(db,email,task_id):
    user = db.users.find_one({'email': email})
    tasks = user.get('tasks', [])
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

def add_task(db,email,new_task):
    new_task['id'] = db.users.find_one({'email': email})['no_of_tasks'] + 1
    print('add.task')
    result = db.users.update_one({'email': email}, {'$set': {'no_of_tasks': new_task['id']}})
    print('update id',result.modified_count)
    if result.modified_count != 1:
        return "Eroor"
    
    result = db.users.update_one({'email': email}, {'$push': {'tasks': new_task}})
    print('update task',result.modified_count)
    
    if result.modified_count == 1:
        return "Ok"
    return "Error"

def delete_task(db,email,task_id):
    result = db.users.update_one({'email': email}, {'$pull': {'tasks': {'id': task_id}}})

    if result.modified_count == 1:
        return "Ok"
    return "Error"

def update_task(db,email,task_id,task):
    if('is_completed' not in task):
      task['is_completed'] = get_task(db,email,task_id)['is_completed']
    print(task)
    result = db.users.update_one({'email': email, 'tasks.id': task_id}, {'$set': {'tasks.$': task}})


def complete_task(db,email,task_id):
    print('complete_task')
    task = get_task(db,email,task_id)
    print(task)
    if task:
        task['is_completed'] = not task['is_completed']
        print(update_task(db,email,task_id,task))
        return "Ok"
    print('complete_task error')
    return "Error"


def get_profile_image(db,email):
    user = db.users.find_one({'email': email})
    print(user)
    image = user.get('profile_image', '')
    return image