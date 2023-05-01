from flask import Flask, request
from flask_cors import CORS, cross_origin
from script import translate_article
from dotenv import load_dotenv
from webscraper import get_article
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def translate():
    url = request.args.get('url')
    bias = request.args.get('bias')
    if not url or not bias:
        return "Missing parameters"
    output = translate_article(url, bias)
    return output

@app.route("/scrape")
@cross_origin()
def scrape():
    url = request.args.get('url')
    if not url:
        return "Missing parameter"
    output = get_article(url)
    return output