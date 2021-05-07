from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, get_flashed_messages
from sqlalchemy.sql.expression import not_, or_
from flask_login import login_required

from my_app.product.model.products import PRODUCTS 
from my_app.product.model.category import Category
from my_app.product.model.product import Product
from my_app import db, rol_admin_need
from my_app.product.model.product import ProductForm

product = Blueprint('product',__name__)

@product.before_request
@login_required
@rol_admin_need
def constructor():
   pass

@product.route('/home')
@product.route('/home/<int:page>')

def home(page=1):
   #print(PRODUCTS.items())
   #print(PRODUCTS.get(1))
   #print(Product.query.all())
   #products = Product.query..filter_by(name="aaaa").paginate(page,5)
   products = Product.query.paginate(page,5)
   return render_template('product/index.html', products = products)


@product.route('/product-create', methods=['POST','GET'])
def create():
   form = ProductForm(meta={
      'csrf':False
   })
   categories = [(c.id,c.name) for c in Category.query.all()]
   form.category_id.choices = categories
   if form.validate_on_submit():
      #print(request.form['name'])
      print(request.form.get('name'))
      #crear
      p = Product(request.form['name'],request.form['price'],request.form['category_id'])
      db.session.add(p)
      db.session.commit()
      flash("Producto creado con exito", category="success")
      return redirect(url_for('product.create'))

   if form.errors:
      flash(form.errors,category="danger")
   
   print(get_flashed_messages())
   return render_template('product/create.html', form=form)


@product.route('/product-update/<int:id>', methods=['POST','GET'])
def update(id):
   form = ProductForm(meta={
      'csrf':False
   })
   categories = [(c.id,c.name) for c in Category.query.all()]
   form.category_id.choices = categories
   product = Product.query.get_or_404(id)
   print(product.category)
   if request.method == 'GET':
      form.name.data = product.name
      form.price.data = product.price
      form.category_id.data = product.category_id
      
   if form.validate_on_submit():
      product.name = form.name.data
      product.price = form.price.data
      product.category_id = form.category_id.data
      #crear
      db.session.add(product)
      db.session.commit()
      flash("Producto actualizado con exito", category="success")
      return redirect(url_for('product.update', id=product.id))

   if form.errors:
      flash(form.errors,category="danger")
   return render_template('product/update.html', product = product, form=form)

@product.route('/product-delete/<int:id>')
def delete(id):
   product = Product.query.get_or_404(id)
   #eliminar
   db.session.delete(product)
   db.session.commit()
   flash("Producto eliminado con exito", category="success")

   return redirect(url_for('product.home'))

@product.route('/product/<int:id>')
def show(id):
   product = Product.query.get_or_404(id)
   return render_template('product/show.html', product = product)

@product.route('/test')
def test():
   #p = Product.query.limit(2).all()
   #p = Product.query.limit(2).first()
   #p = Product.query.order_by(Product.id.desc()).limit(2).all()
   #p = Product.query.order_by(Product.id.desc()).all()
   #p = Product.query.get({"id":2})
   #p = Product.query.filter_by(name="Sandia")
   #p = Product.query.filter_by(name="Hugo", id=1).first()
   #p = Product.query.filter(Product.name.like('S%')).first()
   #p = Product.query.filter(not_(Product.id > 1)).all()
   #p = Product.query.filter(or_(Product.id > 1, Product.name.like('a%'))).all()

   #crear
   #p = Product("creado",93.2)
   #db.session.add(p)
   #db.session.commit()
   
   #actualizar
   #p = Product.query.filter_by(id = 1).first()
   #p.name= "UPDATE1"
   #db.session.add(p)
   #db.session.commit()

   #eliminar
   p = Product.query.filter_by(id = 1).first()
   db.session.delete(p)
   db.session.commit()

   print(p)
   return "Flask"

@product.route('/filter/<int:id>')
def filter(id):
   product = PRODUCTS.get(id)
   if not product:
      abort(404)
   return render_template('product/filter.html', product = product)

@product.app_template_filter('iva')
def iva_filter(product):
   return product["price"] * .20 + product["price"]