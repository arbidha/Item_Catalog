from flask import Flask, render_template ,request ,redirect , url_for ,flash , jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Category, Base, CategoryItem, User

app = Flask(__name__)


# Function shows all catalog items including latest items
@app.route('/')
@app.route('/catalog')
def showCatalog():
    return "This page will show all catalog items with latest added items"

# Function shows all items in a specific category
@app.route('/catalog/<int:category_id>/items')
def showCategoryItem(category_id):
    return "This page will display information about the seleted item from specific category"

# Function shows specific information about that item
@app.route('/catalog/<int:category_id>/<int:item_id>')
def showItem(category_id,item_id):
    return "this page will display information about a specific item"

# Function shows specific information about that item
@app.route('/catalog/new')
def newItem():
    return "this page add a new item"

# Function shows specific information about that item
@app.route('/catalog/<int:category_id>/<int:item_id>/edit')
def editItem(category_id,item_id):
    return "this page edit a Item"

# Function shows specific information about that item
@app.route('/catalog/<int:category_id>/<int:item_id>/delete')
def deleteItem(category_id,item_id):
    return "this page delete a Item"

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded = False)