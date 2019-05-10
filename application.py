from flask import Flask, render_template ,request ,redirect , url_for ,flash , jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , joinedload
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Category, Base, CategoryItem, User


# Import for Google Oauth - login_Session object will work as a dictonary to store values 
from flask import session as login_session

# import used to create pseudo random string to identify each session 
import random
import string

# import for Gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

#Create database and create a session
engine = create_engine('sqlite:///catalogitemwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# ---------------------------------------------------------
# ClientID
# ---------------------------------------------------------

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Item Application"


# ---------------------------------------------------------
# Function to create anti-forgery state token
# ---------------------------------------------------------
# Create anti-forgery state token

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    print "inside gconnect"
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
 	print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
	del login_session['access_token'] 
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    else:
	
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response



# ---------------------------------------------------------
# Function shows all catalog items including latest 5 item
# ---------------------------------------------------------

@app.route('/')
@app.route('/catalog')
def showCatalog():
    category = session.query(Category)
    latestItems = session.query(CategoryItem).order_by(CategoryItem.id.desc()).limit(5)
    if 'username' not in login_session:
        return render_template('publicatalog.html',category = category, latestItems = latestItems)
    else:
        return render_template('catalog.html',category = category, latestItems = latestItems)
    #return "This page will show all catalog items with latest added items"
    #return render_template('catalog.html',category = category, latestItems = latestItems)

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