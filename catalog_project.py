from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_database_setup import Base, ClothingGroup, ClothingItem, User

app = Flask(__name__)

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///clothingstorewithusers.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Functions used for creating and reading user information during session

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

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + 
                    string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

#Authentication with google services

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response.headers['Content-Type'] = 'application/json'
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID"), 401)
        print "Token's ID doesn't match client's ID"
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    login_session['credentials'] = credentials.access_token
    login_session['gplus-id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params={'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)
    print data
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    #Search for previous user and if none exists save user information
    #in user table.

    if getUserID(login_session['email']) == None:
        createUser(login_session)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '</h1>'

    return output

#Disconnecting from google authentication service and wiping user information
#from current session.

@app.route('/gdisconnect')
def gdisconnect():
    print login_session
    access_token = login_session.get('credentials')
    if access_token is None:
        print login_session['username']
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s' % access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus-id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('sayHello'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/')
def sayHello():

    #First check to see if user triggered a 
    #login session

    if login_session:

        #if user has initiated a login session check to see
        #if username is present within the login session
        #this will help determine if user is logged in or out

        if 'username' in login_session:
            user_id = getUserID(login_session['email'])
            user = getUserInfo(user_id)
            print user
            print login_session
            return render_template('hello.html', user=user)
        else: 
            return render_template('hellogeneral.html')
    else:
        return render_template('hellogeneral.html')

@app.route('/clothing/')
def renderItemGroups():
    item_groups = session.query(ClothingGroup).all()
    if login_session:
        if 'username' in login_session:
            return render_template('groups.html', item_groups = item_groups)
        else: 
            return render_template('groupsgeneral.html', item_groups = item_groups)

@app.route('/clothing/JSON')
def itemGroupsJSON():
    item_groups = session.query(ClothingGroup).all()
    return jsonify(ClothingGroup=[i.serialize for i in item_groups])

@app.route('/clothing/<int:clothing_group_id>/')
def renderItemGroupList(clothing_group_id):
    item_group = session.query(ClothingGroup).filter_by(id = clothing_group_id).one()
    items = session.query(ClothingItem).filter_by(item_group_id=clothing_group_id).all()
    if login_session:
        if 'username' in login_session:
            return render_template('itemlist.html', items = items, item_group = item_group)
        else:
            return render_template('itemlistgeneral.html', items = items, item_group = item_group)
    else:
        return render_template('itemlistgeneral.html', items = items, item_group = item_group)

@app.route('/clothing/<int:clothing_group_id>/JSON')
def renderItemGroupListJSON(clothing_group_id):
    item_group = session.query(ClothingGroup).filter_by(id = clothing_group_id).one()
    items = session.query(ClothingItem).filter_by(item_group_id=clothing_group_id).all()
    return jsonify(ClothingItem=[i.serialize for i in items])

@app.route('/clothing/item/<int:item_id>/')
def renderSingleItem(item_id):
    item = session.query(ClothingItem).filter_by(id=item_id).one()
    if login_session:
        if 'username' in login_session:
            return render_template('item.html', item = item)
        else: 
            return render_template('itemgeneral.html', item = item)
    else:
        return render_template('itemgeneral.html', item = item)

@app.route('/clothing/newItemGroup/', methods=['GET', 'POST'])
def addNewItemGroup():
    if 'username' not in login_session:
        return redirect(url_for('/login'))
    if request.method == 'POST':
        user_id = getUserID(login_session['email'])
        newItemGroup = ClothingGroup(name = request.form['name'], user_id = user_id)
        session.add(newItemGroup)
        session.commit()
        return redirect(url_for('renderItemGroups'))
    else:
        return render_template('additemgroup.html')

@app.route('/clothing/<int:clothing_group_id>/newItem', methods=['GET', 'POST'])
def addNewItem(clothing_group_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    clothing_group = session.query(ClothingGroup).filter_by(id = clothing_group_id).one()
    if request.method == 'POST':
        user_id = getUserID(login_session['email'])
        newItem = ClothingItem(name=request.form['name'], description=request.form['description'], price=request.form['price'],
                               size=request.form['size'], color=request.form['color'], item_group_id = clothing_group_id, user_id = user_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('renderItemGroupList', clothing_group_id = clothing_group.id))
    else: 
        return render_template('additem.html', clothing_group = clothing_group)

@app.route('/clothing/<int:clothing_group_id>/edit', methods=['GET', 'POST'])
def editItemGroup(clothing_group_id):
    itemGroup = session.query(ClothingGroup).filter_by(id = clothing_group_id).one()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    user_id = getUserID(login_session['email'])
    if itemGroup.user_id != user_id:
        return redirect(url_for('renderItemGroups'))
    if request.method == 'POST':
        itemGroup.name = request.form['name']
        session.add(itemGroup)
        session.commit()
        return redirect(url_for('renderItemGroups'))
    else: 
        return render_template('editgroup.html', itemGroup = itemGroup)

@app.route('/clothing/item/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')
    changedItem = session.query(ClothingItem).filter_by(id = item_id).one()
    user_id = getUserID(login_session['email'])
    if changedItem.user_id != user_id:
        return redirect(url_for('renderSingleItem', item_id = changedItem.id))
    if request.method == 'POST':
        if request.form['name']:
            changedItem.name = request.form['name']
        if request.form['description']:
            changedItem.description = request.form['description']
        if request.form['size']:
            changedItem.size = request.form['size']
        if request.form['color']:
            changedItem.color = request.form['color']
        if request.form['price']:
            changedItem.price = request.form['price']
        if request.form['picture']:
            changedItem.picture = request.form['picture']
        session.add(changedItem)
        session.commit()
        return redirect(url_for('renderSingleItem', item_id = changedItem.id))
    else: 
        return render_template('edititem.html', item = changedItem)

@app.route('/clothing/<int:clothing_group_id>/delete', methods=['GET', 'POST'])
def deleteItemGroup(clothing_group_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    deletedItemGroup = session.query(ClothingGroup).filter_by(id = clothing_group_id).one()
    user_id = getUserID(login_session['email'])
    if deletedItemGroup.user_id != user_id:
        return redirect(url_for('renderItemGroups'))
    if request.method == 'POST':
        session.delete(deletedItemGroup)
        session.commit()
        return redirect(url_for('renderItemGroups'))
    else: 
        return render_template('deleteitemgroup.html', itemGroup = deletedItemGroup)

@app.route('/clothing/item/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    deletedItem = session.query(ClothingItem).filter_by(id = item_id).one()
    user_id = getUserID(login_session['email'])
    if deletedItem.user_id != user_id:
        return render(url_for('renderSingleItem', item_id = deletedItem.id))
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('renderItemGroupList', clothing_group_id = deletedItem.item_group_id))
    else:
        return render_template('deleteitem.html', item=deletedItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
