import scrapy

from pymongo import MongoClient

class PostSpider(scrapy.Spider):
    name="articles"

    start_urls=[
        'https://www.bbc.com/news'
    ]
    
    # function that will be called when we call scrap crawl
    def parse(self,response):
        articles_title=[]
        articles_text=[]
        articles_date=[]
        articles_url=[]
        client = MongoClient("mongodb+srv://<username>:<password>@cluster0.sml01.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db_articles=client["db_articles"]
        collection_articles = db_articles["collection_articles"]
        for article in response.css('div.nw-c-top-stories'): # get top div
            articles_title=article.css('.gs-c-promo-heading__title::text').getall() # get the text of titles 
            articles_text=article.css('.nw-c-promo-summary::text').getall() # get the description text of the articles
            articles_url=article.css('.gs-c-promo-heading').getall()  # get the urls headings
            articles_date=article.css('.nw-c-promo-meta time').getall() # get the time heading which include date
            for i,item in enumerate(articles_title):
                # we define our dictionary
                dict_articles = {
                'article_title': item,
                'article_text':articles_text[i],
                'article_date':articles_date[i].split('"')[3].split('T')[0],  # we get just the dates so we apply a split  
                'article_url':'https://www.bbc.com/'+articles_url[i].split('"')[3] # we get the article url and we add it to the root url 
                }

                # we add the article information (document) to the collection, and so on for all articles 
                collection_articles.insert_one(dict_articles)



