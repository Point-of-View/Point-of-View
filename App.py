from flask import Flask, request
from flask_cors import CORS
from script import translate_article

app = Flask(__name__)
CORS(app)

@app.route("/")

def translate():
    url = request.args.get('url')
    bias = request.args.get('bias')
    output = translate_article(url, bias)
    return output
