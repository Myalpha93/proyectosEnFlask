from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, get_flashed_messages
from sqlalchemy.sql.expression import not_, or_
from flask_login import login_required

from my_app.product.model.category import Category
from my_app import db, rol_admin_need
from my_app.product.model.category import CategoryForm

category = Blueprint('category',__name__)

@category.before_request
@login_required
@rol_admin_need
def constructor():
   pass

@category.route('/category')
@category.route('/category/<int:page>')
def home(page=1):
   categories = Category.query.paginate(page,5)
   return render_template('category/index.html', categories = categories)


@category.route('/category-create', methods=['POST','GET'])
def create():
   form = CategoryForm(meta={
      'csrf':False
   })
   if form.validate_on_submit():
      #print(request.form['name'])
      print(request.form.get('name'))
      #crear
      p = Category(request.form['name'])
      db.session.add(p)
      db.session.commit()
      flash("Categoria creado con exito", category="success")
      return redirect(url_for('category.create'))

   if form.errors:
      flash(form.errors,category="danger")
   
   print(get_flashed_messages())
   return render_template('category/create.html', form=form)


@category.route('/category-update/<int:id>', methods=['POST','GET'])
def update(id):
   form = CategoryForm(meta={
      'csrf':False
   })
   category = Category.query.get_or_404(id)
   print(category.products)

   if request.method == 'GET':
      form.name.data = category.name
      
   if form.validate_on_submit():
      category.name = form.name.data
      #crear
      db.session.add(category)
      db.session.commit()
      flash("Categoria actualizado con exito", category="success")
      return redirect(url_for('category.update', id=category.id))

   if form.errors:
      flash(form.errors,category="danger")
   return render_template('category/update.html', category = category, form=form)

@category.route('/category-delete/<int:id>')
def delete(id):
   category = Category.query.get_or_404(id)
   #eliminar
   db.session.delete(category)
   db.session.commit()
   flash("Categoryo eliminado con exito", category="success")

   return redirect(url_for('category.home'))

@category.route('/category/<int:id>')
def show(id):
   category = Category.query.get_or_404(id)
   return render_template('category/show.html', category = category)

@category.route('/test')
def test():
   #p = Category.query.limit(2).all()
   #p = Category.query.limit(2).first()
   #p = Category.query.order_by(Category.id.desc()).limit(2).all()
   #p = Category.query.order_by(Category.id.desc()).all()
   #p = Category.query.get({"id":2})
   #p = Category.query.filter_by(name="Sandia")
   #p = Category.query.filter_by(name="Hugo", id=1).first()
   #p = Category.query.filter(Category.name.like('S%')).first()
   #p = Category.query.filter(not_(Category.id > 1)).all()
   #p = Category.query.filter(or_(Category.id > 1, Category.name.like('a%'))).all()

   #crear
   #p = Category("creado",93.2)
   #db.session.add(p)
   #db.session.commit()
   
   #actualizar
   #p = Category.query.filter_by(id = 1).first()
   #p.name= "UPDATE1"
   #db.session.add(p)
   #db.session.commit()

   #eliminar
   p = Category.query.filter_by(id = 1).first()
   db.session.delete(p)
   db.session.commit()

   print(p)
   return "Flask"

@category.route('/filter/<int:id>')
def filter(id):
   category = PRODUCTS.get(id)
   if not category:
      abort(404)
   return render_template('category/filter.html', category = category)

@category.app_template_filter('iva')
def iva_filter(category):
   return category["price"] * .20 + category["price"]