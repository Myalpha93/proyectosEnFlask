from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, get_flashed_messages, session

from my_app import db
from my_app.auth.model.user import LoginForm, User, RegisterForm
auth = Blueprint('auth',__name__)

@auth.route('/register-user', methods=['POST','GET'])
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
        return redirect(url_for('auth.create'))

   if form.errors:
      flash(form.errors,category="danger")
   
   return render_template('auth/create.html', form=form)

@auth.route('/login', methods=['POST','GET'])
def login():
   form = UserForm(meta={
      'csrf':False
   })
   
   if form.validate_on_submit():
      #validar
      user = User.query.filter_by(username=form.username.data).first()
      if user and user.check_password(form.password.data):
          #registrar sesion
          session['username'] = user.username
          session['rol'] = user.rol.value
          session['id'] = user.id
          flash("Bievenido de nuevo " + user.username, category="success")
          return redirect(url_for('product.home'))
      else:
        flash("Uusuario o contraseña incorrecta ", category="danger")
        return redirect(url_for('auth.login'))

   if form.errors:
      flash(form.errors,category="danger")
   
   return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
   session.pop('username')
   session.pop('rol')
   session.pop('id')
   return redirect(url_for('auth.login'))