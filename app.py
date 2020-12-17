from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Setup flask and Mongo
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
mongo.db.mars.drop()

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    
    return redirect("/", code=302)

@app.route("/")
def index():
    data = mongo.db.mars.find_one()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)