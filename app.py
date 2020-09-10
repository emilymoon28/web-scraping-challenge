from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Create an instance of Flask
app = Flask(__name__)

#Use PyMongo to establish mongo connection
#look for the db. if not exist then create
mongo = PyMongo(app,uri="mongodb://localhost:27017/mars_app")

#home page
@app.route("/")
def home():

    #Find the 1st row of data from the mongo 'collection' and store the values as mars_result_doc
    #cretate a collection called 'collection' if it
    mars_result_doc=mongo.db.collection.find_one()

    #'result_doc' is the name will be used in index.html
    return render_template("index.html",result_doc=mars_result_doc)

#this route will trigger the scrape function from scrape_mars.py
@app.route("/scrape")
def scrape():

    # RUN/call the scrape funciton and store the result as 'mars_data
    mars_data = scrape_mars.scrape_info()

    #update the MONGO database using update and insert with no conditions
    mongo.db.collection.update({},mars_data, upsert=True)

    # Redirect back to the home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
