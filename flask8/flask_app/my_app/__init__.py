from flask import Flask, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, current_user, logout_user
from functools import wraps
app = Flask(__name__)

login_manager = LoginManager()
login_manager.__init__(app)
login_manager.login_view = "fauth.login"

def rol_admin_need(f):
   @wraps(f)
   def wrapper(*args,**kwds):
      if current_user.rol.value != "admin":
         logout_user()
         login_manager.unauthorized()
         return redirect(url_for('fauth.login'))
         
         #print('llamando a decorador'+ str(current_user.rol.value))
      return f(*args,**kwds)
   return wrapper

app.config.from_object('configuration.DevelopmentConfig')
db = SQLAlchemy(app)



#from my_app.auth.views import auth
from my_app.fauth.views import fauth
from my_app.product.product import product
from my_app.product.category import category

#vue 
from my_app.spavue.views import spavue
#rest 
from my_app.rest_api.product_api import product_view
from my_app.rest_api.category_api import category_view
#app.register_blueprint(auth)
app.register_blueprint(fauth)
app.register_blueprint(product)
app.register_blueprint(category)
app.register_blueprint(spavue)
db.create_all()



@app.template_filter('mydouble')
def mydoublereverse_filter(n:int):
   return n*2