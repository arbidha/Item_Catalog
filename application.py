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

# ---------------------------------------------------------
# Function shows all catalog items including latest 5 item
# ---------------------------------------------------------

@app.route('/')
@app.route('/catalog')
def showCatalog():
    category = session.query(Category)
    latestItems = session.query(CategoryItem).order_by(CategoryItem.id.desc()).limit(5)
    #return "This page will show all catalog items with latest added items"
    return render_template('catalog.html',category = category, latestItems = latestItems)

# ---------------------------------------------------------
# Function shows all items in a specific category
# ---------------------------------------------------------

@app.route('/catalog/<string:category_name>/items',methods =['GET','POST'])
def showCategoryItem(category_name):
    category = session.query(Category)
    categoryId = session.query(Category).filter_by(name = category_name).one()
    categoryid = categoryId.id
    print categoryid
    categoryItems = session.query(CategoryItem).filter_by(category_id = categoryid).all()
    print categoryItems
    categoryName = session.query(Category).filter_by(id = categoryid).one()
    count = session.query(CategoryItem).filter_by(category_id = categoryid).count()  
    #return "This page will display information about the seleted item from specific category %s ", category_name
    #return "categoryid"
    return render_template('categoryItem.html',category = category, items = categoryItems , categoryName = categoryName, count = count)

# ---------------------------------------------------------
# Function shows specific information about that item
# ---------------------------------------------------------

@app.route('/catalog/<string:category_name>/<int:item_id>')
def showItem(category_name,item_id):
    item = session.query(CategoryItem).filter_by(id = item_id).one()
    print item.description
    #return "this page will display information about a specific item"
    return render_template('item.html',item = item , category_name = category_name )

# ---------------------------------------------------------
# Function to add a new Item 
# ---------------------------------------------------------

@app.route('/catalog/new',methods =['GET','POST'])
def newItem():
    print "inside new item"
    categories = session.query(Category)
    if request.method == 'POST':
        print request.form['category_name']
        category_name = request.form['category_name']
        category_id = session.query(Category).filter_by(name = category_name).one()
        Category.user_id = 1
        new_Item = CategoryItem(title=request.form['title'], description=request.form[
                           'description'], category_id = category_id.id,user_id=Category.user_id)           
        session.add(new_Item)
        session.commit()
        flash("New Menu Created")
        return redirect(url_for('showCatalog'))
    else:
       return render_template('newItem.html', categories = categories)
    #return "this page add a new item"


# ---------------------------------------------------------
# Function to edit a new Item 
# ---------------------------------------------------------
@app.route('/catalog/<string:category_name>/<int:item_id>/edit',methods =['GET','POST'])
def editItem(category_name,item_id):
    print "inside editItem"
    print category_name
    print item_id
    categories = session.query(Category)
    editeditem = session.query(CategoryItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        print("editpost")

        '''Allows user to edit item name'''
        if request.form['name']:
            print("nameeditpost")
            print(request.form['name'])
            editeditem.title = request.form['name']

        '''Allows user to edit item description'''
        if request.form['description']:
            print("description")
            print(request.form['description'])
            editeditem.description = request.form['description']

        '''Allows user to edit item description'''
        if request.form['category']:
            print("category")
            print(request.form['category'])
            editeditem.category_id = request.form['category']

        session.add(editeditem)
        print("add")
        session.commit()
        flash("Item Edited Successfuly")
        return redirect(url_for('showCatalog'))
        #return redirect(url_for('showCategoryItem', category_name = categories.name))
    else:
        return render_template('editItem.html',categories = categories ,category_name = category_name ,item = editeditem  )
    #return "this page edit a Item"
    

# Function shows specific information about that item
@app.route('/catalog/<string:category_name>/<int:item_id>/delete',methods =['GET','POST'])
def deleteItem(category_name,item_id):
    print "inside Delete Item"
    print category_name
    print item_id
    categories = session.query(Category)
    deletedItem = session.query(CategoryItem).filter_by(id = item_id).one()
    print "After Queries"
    '''Allows user to delete item '''
    print(request.method)

    if request.method == 'POST':
        print("deletepost")
        session.delete(deletedItem)
        print(deletedItem)
        session.commit()
        print("commit")
        flash("Item Deleted Successfuly ")
        return redirect(url_for('showCategoryItem', category_name = category_name ))
    else:
        return render_template('deleteItem.html',category = categories,category_name = category_name ,item = deletedItem)

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