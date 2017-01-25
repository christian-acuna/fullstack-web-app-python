from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# create instance of Flask app
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem

engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog/')
def showRestaurants():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('catalog.html', categories=categories)


if __name__ == '__main__':
    # server reloads itself
    app.debug = True
    app.secret_key = 'super_secret_key'
    # use run function to run the local server for our application
    app.run(host = '0.0.0.0', port = 5000)
# if you are importing me from another python module don't do above,
# but still have access to the code
