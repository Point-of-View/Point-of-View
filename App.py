from flask import Flask, request
from script import translate_article

app = Flask(__name__)

@app.route("/")

def translate():
    url = request.args.get('url')
    bias = request.args.get('bias')
    output = translate_article(url, bias)
    return output
