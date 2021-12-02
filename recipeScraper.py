from flask import Flask, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app)  # Prevents the raising of restrictions due to CORS

def grabRecipeLinks(html):
    """Finds three recipe links on html Page from Allrecipes returns 
    them in a dictionary with the title of the recipe as the key"""
    links = html.find_all('a', class_='card__titleLink manual-link-behavior')
    linkColl = {}
    for a in links:
        if len(linkColl) < 3:
            recipeTitle = a['title']
            recipeUrl = a['href']
            linkColl[recipeTitle] = recipeUrl
    return linkColl

def scrapeRecipe(ingredientName):
    """Takes an ingredient name and returns a dictionary with three 
    recipe links scrpaed from Allrecipes"""
    ingredientName = ingredientName.replace(" ", "+")
    url = 'https://www.allrecipes.com/search/results/?search=' + ingredientName
    resp = requests.get(url)
    htmlDocument = BeautifulSoup(resp.content, "html.parser")
    linkDict = grabRecipeLinks(htmlDocument)
    return linkDict

@app.route('/recipeScraper/<string:ingredientName>', methods=['Get'])
def wikiScraper(ingredientName: str):
    resp = scrapeRecipe(ingredientName)
    return jsonify(resp)

if __name__ == '__main__':
    app.run(port=3033)
