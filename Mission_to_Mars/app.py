from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Setup Mongo Connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    mars_data = mongo.db.collection.find_one()

    return render_template("index.html", mars = mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run scrape function
    mars_dict = scrape_mars.scrape_all()

    # Update Mongo Database
    mongo.db.collection.update({}, mars_dict, upsert=True)

    # Redirect to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
