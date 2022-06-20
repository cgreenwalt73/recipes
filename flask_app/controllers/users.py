from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt= Bcrypt(app)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_user():
    if not User.validate_user_registration(request.form):
        return redirect('/')
    else:
        hash_pass = bcrypt.generate_password_hash(request.form['password'])
        data= {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'].lower(),
            'password' : hash_pass
        }
        session['user_id'] = User.add_user(data)
        return redirect('/dashboard')

@app.route('/dashboard')
def show_user_page():
    if 'user_id' not in session:
        return redirect('/logout')
    user_dashboard= User.get_user_by_id(session['user_id'])
    all_recipes = Recipe.get_all_recipes()
    return render_template('dashboard.html', user_dashboard=user_dashboard, all_recipes=all_recipes)

@app.route('/login', methods=['POST'])
def user_login():
    if not User.validate_user_login(request.form):
        return redirect('/')
    else:
        return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


