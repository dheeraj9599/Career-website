from flask import Flask, render_template, request, redirect, session, flash
from db import load_users, check_valid_user, register_new_user, Load_Jobs_From_DB, add_job_to_DB,fetch_job_with_id, add_updated_job_to_DB, add_application_in_DB
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def login():
    # print(response)
    if 'user_id' in session:
        return redirect('/home')
    elif 'admin_id' in session:
        return redirect('/admin')
    else:
        return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' in session or 'admin_id' in session:
        jobs = Load_Jobs_From_DB()
        return render_template('user/home.html', jobs = jobs)
    else:
        return redirect('/')


@app.route('/admin')
def admin():
    if 'admin_id' in session:
        jobs = Load_Jobs_From_DB()
        return render_template('admin/admin.html', jobs = jobs)
    else:
        return redirect('/')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    type = request.form.get('type')
    if type == "As a Admin": type = "admin"
    else: type = "users"

    user = check_valid_user(type, email, password)
    if len(user) > 0 and type == "users":
        session['user_id'] = user[0]['userid']
        return redirect('/home')
    elif len(user) > 0 and type == "admin":
        session['admin_id'] = user[0]['admin_id']
        return redirect('/admin')
    else:
        flash("Invalid username or Password")
        return redirect('/')



@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register_user', methods=['POST'])
def register_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    type = request.form.get('type')
    if type == "As a Admin": type = "admin"
    else: type = "users"
    print(type)
    register_new_user(type, name, email, password)

    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/logout_admin')
def logout_admin():
    session.pop('admin_id')
    return redirect('/')


@app.route('/add_new_job')
def add__new_job():
    if 'admin_id' in session:
        return render_template('admin/add/add_new_job.html')
    else:
        return redirect('/admin') 


@app.route('/submit_new_job', methods=['POST'])
def submit_new_job():
    title = request.form.get('title')
    location = request.form.get('location')
    salary = request.form.get('salary')
    currency = request.form.get('currency')
    responsibilities = request.form.get('responsibilities')
    requirements = request.form.get('requirements')
    add_job_to_DB(title, location, salary, currency, responsibilities, requirements)
    return redirect('/admin')


@app.route('/update_job')
def update_job():
    jobs = Load_Jobs_From_DB()

    if 'admin_id' in session:
        return render_template('admin/update/update_job.html', jobs = jobs)
    else:
        return redirect('/admin') 
    


@app.route('/update_job/<id>')
def update_specific_job(id):
    job = fetch_job_with_id(id)
    if 'admin_id' in session:
        return render_template('admin/update/update_specific_job.html', job = job)
    else:
        return redirect('/admin') 

@app.route('/<id>/submit_updated_job', methods=['POST'])
def submit_updated_job(id):
    title = request.form.get('title')
    location = request.form.get('location')
    salary = request.form.get('salary')
    currency = request.form.get('currency')
    responsibilities = request.form.get('responsibilities')
    requirements = request.form.get('requirements')
    add_updated_job_to_DB(title, location, salary, currency, responsibilities, requirements,id)
    return redirect('/update_job')


@app.route('/job/<id>')
def job_application(id):
    job = fetch_job_with_id(id)
    if 'user_id' in session:
        return render_template('user/job_application.html', job = job)
    else : redirect('/')
    
@app.route('/job/<id>/apply', methods=['POST'])
def job_application_submission(id):
    Full_name = request.form.get('Full_name')
    email = request.form.get('email')
    Education = request.form.get('Education')
    Work_Experience = request.form.get('Work_Experience')
    Resume_url = request.form.get('Resume_url')
    if 'user_id' in session:
        add_application_in_DB(id, Full_name, email, Education, Work_Experience, Resume_url)
        return render_template('user/submitted_application.html')
    else : redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
