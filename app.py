from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# set up mongo
# conn = 'mongodb://localhost:27017'
# client = PyMongo.MongoClient(conn)
# db = client.mars_data

# db.info.insert_one()
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")


# Route to render index.html template using data from Mongo
## THIS NEEDS WORK!!!!!
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_info = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info) 


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)