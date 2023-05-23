from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS, cross_origin

from script import translate_article
from webscraper import get_article


# Load environment variables
load_dotenv()

# Set up Flask
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Flask route for main functionality
@app.route("/")
@cross_origin()
def translate():
    url = request.args.get('url')
    bias = request.args.get('bias')
    if not url or not bias:
        return "Missing parameters"
    output = translate_article(url, bias)
    return output


# Flask route to perform webscraping
@app.route("/scrape")
@cross_origin()
def scrape():
    url = request.args.get('url')
    if not url:
        return "Missing parameter"
    output = get_article(url)
    return output
