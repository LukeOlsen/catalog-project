from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_database_setup import Base, ClothingGroup, ClothingItem

app = Flask(__name__)

engine = create_engine('sqlite:///clothingstore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def sayHello():
    return render_template('hello.html')

@app.route('/clothing')
def renderItemGroups():
    item_groups = session.query(ClothingGroup).all()
    return render_template('groups.html', item_groups = item_groups)

@app.route('/clothing/<int:clothing_group_id>/')
def renderItemGroupList(clothing_group_id):
    item_group = session.query(ClothingGroup).filter_by(id = clothing_group_id).one()
    items = session.query(ClothingItem).filter_by(item_group_id = item_group.id)
    return render_template('itemlist.html', items = items)

@app.route('clothing/<int:clothing_group_id>/<int:item_id>/')
def renderItem(clothing_group_id, item_id):
    return render_template('item.html', clothing_group_id = clothing_group_id, item_id = item_id)

@app.route('/clothing/newItemGroup/', methods=['GET', 'POST'])
def addNewItemGroup():
    if request.method == 'POST':
        pass
    else:
        return render_template('additemgroup.html')

@app.route('/clothing/<int:clothing_group_id>/newItem', methods=['GET', 'POST'])
def addNewItem(clothing_group_id):
    if request.method == 'POST':
        pass
    else: 
        return render_template('additem.html')

@app.route('/clothing/<int:clothing_group_id>/edit', methods=['GET', 'POST'])
def editItemGroup(clothing_group_id):
    if request.method == 'POST':
        pass
    else: 
        return render_template('editgroup.html')

@app.route('/clothing/<int:clothing_group_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(clothing_group_id, item_id):
    if request.method == 'POST':
        pass
    else: 
        return render_template('edititem.html')

@app.route('/clothing/<int:clothing_group_id>/delete', methods=['GET', 'POST'])
def deleteItemGroup(clothing_group_id):
    if request.method == 'POST':
        pass
    else: 
        return render_template('deleteitemgroup.html')

@app.route('/clothing/<int:clothing_group_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(clothing_group_id, item_id):
    if request.method == 'POST':
        pass
    else:
        return render_template('deleteitem.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
