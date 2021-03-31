#import modules and libraries
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
#initialization of the API
app = Flask(__name__)
api = Api(app)

# load the database
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.sml01.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

#connect to database
db_articles=client["db_articles"]




collection_articles = db_articles["collection_articles"]
# Define endpoint for listing all the articles on the db
class FindAll(Resource):
    def get(self):
        # query to find documents in our collection
        articles = collection_articles.find({},{"_id":0})
        articles_collection={}
        # assign a number to article 
        for i,article in enumerate(articles):
            articles_collection["article %i "%i]=article
        return {'Top news  on bbc.com/news':articles_collection}
        


# Define endpoint for listing all the articles on the db the contains the keyword desired

class FindByKey(Resource):
    def get(self, key):
        # find all articles in our articles collection
        articles_key = collection_articles.find({},{"_id":0})
        collections={}
        for i,article in enumerate(articles_key):
            # we test if the article contains the keyword
            if str(article).find(key) > 0:  # if true str.find(key) return a positif number else -1
                collections[i]=article
        return collections
   
   # pass


api.add_resource(FindAll, '/')  # '/' is our entry point for articles
api.add_resource(FindByKey, "/<string:key>")  # and '/lkey' is our entry point for articles contains keyword


if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app