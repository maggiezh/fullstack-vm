from db_setup import Base, User, Category, Item
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from flask_httpauth import HTTPBasicAuth
import json
import random, string
from flask import session as login_session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
from flask import (
    Flask, 
    flash, 
    jsonify, 
    request, 
    url_for, 
    abort, 
    g, 
    render_template, 
    make_response,
    redirect
)

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('/var/www/html/catalog/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Manager"

# Connect to Database and create database session
engine = create_engine('postgresql://catalog:catalog@localhost/catalogMngr')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Homepage
@app.route('/')
@app.route('/catalog')
def getCatalog():
    catalog = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(10)
    return render_template('catalog.html', catalog=catalog, items=items)

# JSON APIs to view catalog
@app.route('/catalog/JSON')
def catalogJSON():
    catalog = session.query(Category).all()
    return jsonify(category=[i.serialize for i in catalog])

#Login page
""" 
    Login page to authenticate an user
    Returns: Page for user to login.
"""
@app.route('/catalog/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# gconnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
     # Validate state token
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
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
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
    login_session['email'] = data['email']

    # see if user exists and if it doesn't, make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'

    flash("you are now logged in as %s" % login_session['username'])
    return output

#gdisconnect
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
           % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps\
                   ('You are successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    else:
        response = make_response(json.dumps\
                   ('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
    return response


""" 
    Display list of items for a category
    Args: category_id to identify the category selected by user
    Returns: Page displaying the list of items for a selected category
"""
@app.route('/catalog/<int:category_id>/items')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    catalog = session.query(Category).all()
    isLoggedIn = 'username' in login_session
    items = session.query(Item).filter_by(
            category_id=category.id).all()
    return render_template('category.html', 
                            items=items, 
                            category=category, 
                            catalog=catalog, 
                            isLoggedIn = isLoggedIn)
 
# JSON APIs to view all the items
@app.route('/catalog/items/JSON')
def itemListJSON():
    items = session.query(Item).all()
    return jsonify(catalogItems=[i.serialize for i in items])

# JSON APIs to view list of items for a category
@app.route('/catalog/<int:category_id>/items/JSON')
def catalogItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(catalogItems=[i.serialize for i in items])

@app.route('/catalog/<int:category_id>/items/<int:item_id>')
def showCategoryItem(category_id, item_id):
    isLoggedIn = 'username' in login_session
    category = session.query(Category).filter_by(id=category_id).first()
    categoryItem = session.query(Item).filter_by\
                   (id = item_id, category_id=category_id).first()
    return render_template('item.html', item = categoryItem, \
                           isLoggedIn=isLoggedIn)

""" 
    Create new category item to the database
    Returns: on GET: Page to create a new item.
             on POST: Redicrect to main page after item has been created. 
             Login page when user is not signed in.
"""
@app.route('/catalog/items/new', methods=['GET', 'POST'])
def addItem():
    #Only authorized user can add new item
    if 'username' not in login_session:
        flash("Only authorized user can add new item.")
        return redirect('/catalog/login')
    catalog = session.query(Category).all()
    if request.method == 'POST':
        newItem = Item(
            itemName = request.form['itemName'],
            description = request.form['description'],
            category_id = request.form['category_id'],
            user_id = login_session['user_id']
        )
        session.add(newItem)
        session.commit()
        flash("New Item %s is successfully added." % (newItem.itemName))
        return redirect(url_for('showCategory', \
                        category_id = request.form['category_id']))
    else:
        return render_template('newItem.html', catalog=catalog)

""" 
    Edit an existing item
    Args: item_id: identify the item to update.
    Returns: 
    On POST: Update the item, then redirect to the page to show the update item list  
    On GET:  Display the page for user to edit an item
"""
@app.route('/catalog/items/<int:item_id>/edit', methods=['GET','POST'])
def editItem(item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    # First check if the user is authenticated
    isLoggedIn = 'username' in login_session
    # If the user is not authenticated
    if not isLoggedIn:
        flash("Only authorized user can update item. Please login first.")
        return redirect('/catalog/login')
    # Check if the user is authorzied
    isAuthorized = login_session['user_id'] == editedItem.user_id
    if not isAuthorized:
        return "<script>function myFunction() \
        {alert('You can only edit items you own.');}\
        </script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['itemName']:
            editedItem.itemName = request.form['itemName']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Item %s Successfully Edited' % (editedItem.itemName))
        return redirect(url_for('showCategory', \
                       category_id = editedItem.category_id))
    else:
        return render_template('editItem.html', item_id=item_id, \
                               item=editedItem)

""" 
    Delete category item to the database
    Args: item_id: identify the item that needs to be removed
    Returns: on GET: Page to create a new item.
             on POST: Redicrect to main page after item has been created. 
             Login page when user is not signed in.
"""
@app.route('/catalog/items/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    # First check if the user is authenticated
    isLoggedIn = 'username' in login_session
    # If the user is not authenticated
    if not isLoggedIn:
        flash("Only authorized user can update item. Please login first.")
        return redirect('/catalog/login')
    # Check if the user is authorzied
    isAuthorized = login_session['user_id'] == itemToDelete.user_id
    if not isAuthorized:
        return "<script>function myFunction() \
        {alert('You can only delete items you own.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showCategory', \
                        category_id=itemToDelete.category_id))
    else:
        return render_template('deleteItem.html', 
                                item_id=item_id, 
                                item=itemToDelete)

""" 
    Creates a new user in the database.
    Args: login_session: session object with user data.
    Returns: user.id: generated distinct integer value 
    identifying the newly created user.
"""
def createUser(login_session):
    newUser = User(username=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

""" 
    Gets user information by user_id.
    Args: user_id
    Returns: user object with user data
"""
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

""" 
    Gets user_id by user's email.
    Args: email
    Returns: user_id
"""
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except NoResultFound:
        return None

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
