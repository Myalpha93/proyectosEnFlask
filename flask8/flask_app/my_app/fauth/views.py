from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, get_flashed_messages, session

from my_app import db, login_manager
from my_app.auth.model.user import LoginForm, User, RegisterForm
fauth = Blueprint('fauth',__name__)

from flask_login import login_user, logout_user, current_user, login_required

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(user_id)

@fauth.route('/register-user', methods=['POST','GET'])
def create():
   form = RegisterForm(meta={
      'csrf':False
   })
   #if session.get['username']:
   if 'username' in session:
       print(session)

   if form.validate_on_submit():
      #crear
      if User.query.filter_by(username=form.username.data).first():
          flash("Usuario existente", category="danger")
      else:
        p = User(form.username.data,form.password.data)
        db.session.add(p)
        db.session.commit()
        flash("Usuario creado con exito", category="success")
        return redirect(url_for('fauth.create'))

   if form.errors:
      flash(form.errors,category="danger")
   
   return render_template('auth/create.html', form=form)

@fauth.route('/login', methods=['POST','GET'])
def login():
   if current_user.is_authenticated:
      flash("Ya has iniciado sesion" , category="danger")
      return redirect(url_for('product.home'))
   
   form = LoginForm(meta={ 'csrf':False})
   
   if form.validate_on_submit():
      #validar
      user = User.query.filter_by(username=form.username.data).first()
      if user and user.check_password(form.password.data):
         #registrar sesion
         login_user(user)
         flash("Bievenido de nuevo " + user.username, category="success")
         next = request.form['next']
         #if not if_safe_url(next):
         #   return flask.abort(400)
         print(next)
         return redirect(next or url_for('product.home'))
      else:
        flash("Uusuario o contraseña incorrecta ", category="danger")
        return redirect(url_for('fauth.login'))

   if form.errors:
      flash(form.errors,category="danger")
   
   return render_template('auth/login.html', form=form)

@fauth.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('fauth.login'))

@fauth.route('/protegido')
@login_required
def protegido():
   return "Vista Protegida"