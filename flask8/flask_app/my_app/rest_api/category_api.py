import json
from flask import request
from flask.views import MethodView
from my_app.rest_api.helper.request import sendResJson
from my_app.product.model.category import Category
from my_app import app, db

class CategoryApi(MethodView):

    def get(self, id=None):
        categories = Category.query.all()
        if id:
            categories = Category.query.get(id)
            res = CategoryToJson(categories)
        else:
            res = []
            for p in categories:
                res.append(CategoryToJson(p))
        return sendResJson(res, None,200)
    
    
def CategoryToJson(category:Category):
    return {
                'id':category.id,
                'name':category.name
            }

category_view = CategoryApi.as_view('category_view')
app.add_url_rule('/api/category/', view_func=category_view,methods=['GET'])
app.add_url_rule('/api/category/<int:id>', view_func=category_view,methods=['GET'])