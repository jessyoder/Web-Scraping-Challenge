from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri='mongodb://localhost:27017/')

@app.route("/")
def index():



@app.route("/scrape")



if __name__ == "__main__":
    app.run(debug=True)