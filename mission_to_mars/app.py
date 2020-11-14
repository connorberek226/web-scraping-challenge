from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

mongo = PyMongo(app)

@app.route("/")
def dashboard():

    try:
        mars_data = list(mongo.db.collection.fin())
    except:
        mars_data = {}

    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scrape():

    mars = scrape_mars.scrape()


    mars_dict = {
        "news_title": mars["news_title"],
        "news_p": mars["news_p"],
        "featured_image_url": mars["featured_image_url"],
        "mars_factoids": mars["mars_factoids"],
        "hemisphere_image_urls": mars["hemisphere_image_url"]
    }

    # Insert mars_dict into database
    mongo.db.collection.insert_one(mars_dict)

    # Redirect back to home page
    return redirect("http://localhost:8000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)