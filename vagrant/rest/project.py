from flask import Flask
# create instance of Flask app
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
# leave in the trailing slash and flask will render the page even when it is not there
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(resturant_id = restaurant.id)
    output = ''
    for i in items:
        output += i.name
        output += ' | %s' % i.id
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br>'
        output += '</br>'

    return output

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    output = ''
    output += "<form action='/new' method='POST' enctype='multipart/form-data'>"
    output += "<h2>Add Menu Item to %s</h2>" % (restaurant.name)
    output += "<input type='text' name='item' placeholder='Menu Item' /><input type='submit' value='Submit' /></form>"
    return output


# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"
# if you are executing me with the python interperter
# do this
if __name__ == '__main__':
    # server reloads itself
    app.debug = True
    # use run function to run the local server for our application
    app.run(host = '0.0.0.0', port = 5000)
# if you are importing me from another python module don't do above,
# but still have access to the code
