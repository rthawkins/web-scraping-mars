import pymongo
import scrape_mars
from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# conn = 'mongodb://localhost:27017/mars_db'
# client = pymongo.MongoClient(conn)

# # Declare the database
# db = client.mars_db

# # Declare the collection
# collection = db.mars_stuff

# mars_dict = mongo.db.mars_stuff.find_one()




#################################################
# Flask Routes
#################################################

@app.route("/scrape")
def scrape():
    # Create our session (link) from Python to the DB
    mars_dict = mongo.db.mars_dict
    mars_new_data = scrape_mars.scrape()
    mars_dict.update({}, mars_new_data, upsert=True)
    return redirect("/", code=302)

@app.route("/")
def welcome():
    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars_dict=mars_dict)

if __name__ == '__main__':
    app.run(debug=True)
