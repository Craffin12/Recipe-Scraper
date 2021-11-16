from flask import Flask, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app)  # Prevents the raising of restrictions due to CORS


def grabRecipe(html):
    links = html.find_all('a', class_='card__titleLink manual-link-behavior')

    linkColl = {}

    count = 0

    for a in links:
        recipeTitle = a['title']
        recipeUrl = a['href']
        linkColl[recipeTitle] = recipeUrl

    return linkColl


def scrapeRecipe(ingredientName):
    """
    """
    ingredientName = ingredientName.replace(" ", "+")
    url = 'https://www.allrecipes.com/search/results/?search=' + ingredientName

    res = requests.get(url)

    html = BeautifulSoup(res.content, "html.parser")

    linkDict = grabRecipe(html)

    return linkDict


@app.route('/recipeScraper/<string:ingName>', methods=['Get'])
def wikiScraper(ingName: str):
    resp = scrapeRecipe(ingName)
    return jsonify(resp)


if __name__ == '__main__':
    app.run(port=3033)
