from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_database_setup import Base, ClothingGroup, ClothingItem

app = Flask(__name__)

engine = create_engine('sqlite:///clothingstore.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def sayHello():
    return render_template('hello.html')

@app.route('/clothing/')
def renderItemGroups():
    item_groups = session.query(ClothingGroup).all()
    return render_template('groups.html', item_groups = item_groups)

@app.route('/clothing/<int:clothing_group_id>/')
def renderItemGroupList(clothing_group_id):
    item_group = session.query(ClothingGroup).filter_by(id = clothing_group_id).one()
    items = session.query(ClothingItem).filter_by(item_group_id = item_group.id)
    return render_template('itemlist.html', items = items, item_group = item_group)

@app.route('/clothing/<int:clothing_group_id>/<int:item_id>/')
def renderSingleItem(item_id):
    item = session.query(ClothingItem).filter_by(id=item_id).one()
    return render_template('item.html', item = item)

@app.route('/clothing/newItemGroup/', methods=['GET', 'POST'])
def addNewItemGroup():
    if request.method == 'POST':
        newItemGroup = ClothingGroup(name = request.form['name'])
        session.add(newItemGroup)
        session.commit()
        return redirect(url_for('renderItemGroups'))
    else:
        return render_template('additemgroup.html')

@app.route('/clothing/<int:clothing_group_id>/newItem', methods=['GET', 'POST'])
def addNewItem(clothing_group_id):
    clothing_group = session.query(ClothingGroup).filter_by(id = clothing_group_id).one()
    if request.method == 'POST':
        newItem = ClothingItem(name=request.form['name'], description=request.form['description'], price=request.form['price'],
                               size=request.form['size'], color=request.form['color'], item_group_id = clothing_group_id)
        session.add(newItem)
        session.commit()
    else: 
        return render_template('additem.html', clothing_group = clothing_group)

@app.route('/clothing/<int:clothing_group_id>/edit', methods=['GET', 'POST'])
def editItemGroup(clothing_group_id):
    if request.method == 'POST':
        itemGroup = session.query(ClothingGroup).filter_by(id = clothing_group_id).one()
        itemGroup.name = request.form['name']
        session.add(itemGroup)
        session.commit()
    else: 
        return render_template('editgroup.html')

@app.route('/clothing/item/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id):
    changedItem = session.query(ClothingItem).filter_by(id = item_id).one()
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
        session.add(changedItem)
        session.commit()
        redirect(url_for('renderItem', item_id = changedItem.id))
    else: 
        return render_template('edititem.html', item = changedItem)

@app.route('/clothing/<int:clothing_group_id>/delete', methods=['GET', 'POST'])
def deleteItemGroup(clothing_group_id):
    deletedItemGroup = session.query(ClothingGroup).filter_by(id = clothing_group_id).one()
    if request.method == 'POST':
        session.delete(deletedItemGroup)
        session.commit()
        return redirect(url_for('renderItemGroups'))
    else: 
        return render_template('deleteitemgroup.html', itemGroup = deletedItemGroup)

@app.route('/clothing/<int:clothing_group_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(clothing_group_id, item_id):
    deletedItem = session.query(ClothingItem).filter_by(id = item_id).one()
    itemGroup = session.query(ClothingGroup).filter_by(id = clothing_group_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('renderItemGroupList', clothing_group_id = clothing_group_id))
    else:
        return render_template('deleteitem.html', item=deleteItem, itemGroup = itemGroup)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
