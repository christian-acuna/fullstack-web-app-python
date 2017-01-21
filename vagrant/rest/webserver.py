from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

import cgi

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += '<html><body>'
                output += 'Hello!'
                output += "<form action='/hello' method='POST' enctype='multipart/form-data'><h2>What would you like me to say?</h2><input type='text' name='message' /><input type='submit' value='Submit' /></form>"
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += '<html><body>'
                output += "&#161Hola! <a href='/hello'>Back to hello</a>"
                output += "<form action='/hello' method='POST' enctype='multipart/form-data'><h2>What would you like me to say?</h2><input type='text' name='message' /><input type='submit' value='Submit' /></form>"
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                output = ""
                output += '<html><body>'
                output += "<h1>Restaurants</h1>"
                output += '<h2><a href="/restaurants/new">Make a New Restaurant</a></h2>'
                for restaurant in restaurants:
                    output += "%s | %s" % (restaurant.name, restaurant.id)
                    output += "<br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "<br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a><br><br>" % restaurant.id

                output += '</body></html>'
                self.wfile.write(output)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                output = ""
                output += '<html><body>'
                output += "<h1>Create a new Restaurant</h1>"
                output += "<form action='/restaurants/new' method='POST' enctype='multipart/form-data'><input type='text' name='name' placeholder='New Restaurant Name'/><input type='submit' value='Submit' /></form>"
                output += '</body></html>'
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurant_id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id = int(restaurant_id)).one()
                print restaurant.name

                if restaurant != [] :

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += '<html><body>'
                    output += "<h1>Edit Restaurant</h1>"
                    output += "<form action='/restaurants/%s/edit' method='POST' enctype='multipart/form-data'><input type='text' name='name' placeholder='New Restaurant Name' value='%s'/><input type='submit' value='Submit' /></form>" % (restaurant.id, restaurant.name)
                    output += '</body></html>'
                    self.wfile.write(output)
                    return

            if self.path.endswith("/delete"):
                restaurant_id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id = int(restaurant_id)).one()
                print restaurant.name

                if restaurant != [] :

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += '<html><body>'
                    output += "<h1>Are you sure you want to delete %s?</h1>" % (restaurant.name)
                    output += "<form action='/restaurants/%s/delete' method='POST' enctype='multipart/form-data'><input type='submit' value='Delete' /></form>" % (restaurant.id)
                    output += '</body></html>'
                    self.wfile.write(output)
                    return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/new"):

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('name')
                    newRestaurant = Restaurant(name = restaurant_name[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                restaurant_id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id = int(restaurant_id)).one()
                # print restaurant.name

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('name')
                if restaurant != []:
                    restaurant.name = restaurant_name[0]
                    session.add(restaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()

            if self.path.endswith("/delete"):
                restaurant_id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id = int(restaurant_id)).one()
                print restaurant.name

                if restaurant != []:
                    session.delete(restaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()
        except:
            pass
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        # keep it constantly listening
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
