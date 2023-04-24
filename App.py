from flask import Flask, request
from flask_cors import CORS, cross_origin
from script import translate_article
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def translate():
    url = request.args.get('url')
    bias = request.args.get('bias')
    output = translate_article(url, bias)
    return output