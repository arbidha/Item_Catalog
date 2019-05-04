from flask import Flask, render_template ,request ,redirect , url_for ,flash , jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , joinedload
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Category, Base, CategoryItem, User

app = Flask(__name__)

#Create database and create a session
engine = create_engine('sqlite:///catalogitemwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Function shows all catalog items including latest items
@app.route('/')
@app.route('/catalog')
def showCatalog():
    category = session.query(Category)
    latestItems = session.query(CategoryItem).order_by(CategoryItem.id.desc()).limit(5)
    #return "This page will show all catalog items with latest added items"
    return render_template('catalog.html',category = category, latestItems = latestItems)

# Function shows all items in a specific category
@app.route('/catalog/<int:category_id>/items')
def showCategoryItem(category_id):
    return "This page will display information about the seleted item from specific category"
    #return render_template('categoryItem.html',category = category)

# Function shows specific information about that item
@app.route('/catalog/<int:category_id>/<int:item_id>')
def showItem(category_id,item_id):
    return "this page will display information about a specific item"
    #return render_template('item.html',category = category)

# Function shows specific information about that item
@app.route('/catalog/new')
def newItem():
    return "this page add a new item"
    #return render_template('newItem.html',category = category)

# Function shows specific information about that item
@app.route('/catalog/<int:category_id>/<int:item_id>/edit')
def editItem(category_id,item_id):
    return "this page edit a Item"
    #return render_template('editItem.html',category = category)

# Function shows specific information about that item
@app.route('/catalog/<int:category_id>/<int:item_id>/delete')
def deleteItem(category_id,item_id):
    return "this page delete a Item"
    #return render_template('deleteItem.html',category = category)

# --------------------------------------
# JSON APIs to show Catalog information
# --------------------------------------

@app.route('/catalog/catalog.json')
def catalogsJSON():
    """Returns JSON of all items in catalog"""
    categories = session.query(Category).options(joinedload(Category.items)).all()
    return jsonify(Category = [dict(c.serialize, items=[i.serialize for i in c.items])
                         for c in categories])

@app.route('/catalog/<int:category_id>/JSON')
def catalogJSON(category_id):
    """Returns JSON of selected item in catalog"""
    category = session.query(Category).options(joinedload(Category.items)).filter_by(id=category_id).all()
    return jsonify(Category = [dict(c.serialize, items=[i.serialize for i in c.items])
                         for c in category])

@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def catalogItemJSON(category_id, item_id):
    """Returns JSON of selected item in catalog"""
    catalogItem = session.query(CategoryItem).filter_by(id=item_id).one()
    return jsonify(Catalog_Item=catalogItem.serialize)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded = False)