from flask import Flask, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
import requests

application = Flask(__name__)

CORS(application)  # Prevents the raising of restrictions due to CORS

"""
Used the official documentation 
https://beautiful-soup-4.readthedocs.io/en/latest/
to research general beautifulsoup 4 methods. All code is my own.

Used the offical documentation
https://docs.python-requests.org/en/latest/user/quickstart/
to learn how to use requests and to learn about response.text.
All code is my own.
"""

def grabRecipeLinks(html):
    """Finds three recipe links on html Page from Allrecipes returns 
    them in a dictionary with the title of the recipe as the key"""
    links = html.find_all("a", class_="card__titleLink manual-link-behavior")
    linkColl = {}
    for a in links:
        if len(linkColl) < 3:
            recipeTitle = a["title"]
            recipeUrl = a["href"]
            linkColl[recipeTitle] = recipeUrl
    return linkColl

def requestPageGetHtml(url):
    """Requests text information from url page and returns None if status code is 404 or
    an Beautiful soup object that contains page"s html"""
    resp = requests.get(url)
    resp = resp.text
    return BeautifulSoup(resp, "html.parser")

def scrapeRecipes(ingredientName):
    """Takes an ingredient name and returns a dictionary with three 
    recipe links scraped from Allrecipes"""
    ingredientName = ingredientName.replace(" ", "+")
    url = "https://www.allrecipes.com/search/results/?search=" + ingredientName
    htmlDocument = requestPageGetHtml(url)
    linkDict = grabRecipeLinks(htmlDocument)
    return linkDict

@application.route("/recipeScraper/<string:ingredientName>", methods=["Get"])
def wikiScraper(ingredientName: str):
    resp = scrapeRecipes(ingredientName)
    return jsonify(resp)

if __name__ == "__main__":
    application.run("127.0.0.1", 3033)
