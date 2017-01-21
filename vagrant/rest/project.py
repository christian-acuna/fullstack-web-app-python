from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# create instance of Flask app
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant = restaurant).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id  = menu_id).one()
    return jsonify(MenuItem=item.serialize)

# leave in the trailing slash and flask will render the page even when it is not there
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(resturant_id = restaurant.id)

    return render_template('menu.html', restaurant = restaurant, items = items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant = restaurant)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant.id))
    else:
        return render_template('newmenuitem.html', restaurant = restaurant)


# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        menu_item.name = request.form['name']
        session.add(menu_item)
        session.commit()
        flash("Menu Item successfully edited!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant.id))
    else:
        return render_template('editmenuitem.html', restaurant = restaurant, menu_item = menu_item)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(menu_item)
        session.commit()
        flash("Menu Item successfully deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant.id))
    else:
        return render_template('deletemenuitem.html', restaurant_id = restaurant.id, item = menu_item)


if __name__ == '__main__':
    # server reloads itself
    app.debug = True
    app.secret_key = 'super_secret_key'
    # use run function to run the local server for our application
    app.run(host = '0.0.0.0', port = 5000)
# if you are importing me from another python module don't do above,
# but still have access to the code
