import requests
from bs4 import BeautifulSoup
import sys

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

def get_article(url):
    if not ("cnn.com" in url or "foxnews.com" in url):
        return
    
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    if "cnn.com" in url:
        return get_cnn_article(soup)
    elif "foxnews.com" in url:
        return get_fox_article(soup)


def get_cnn_article(soup):
    content = soup.find_all("p", {"class:", "paragraph"})
    text = "\n\n".join([p.text.strip() for p in content])
    article = {"source": "CNN", "text": text}
    return article

def get_fox_article(soup):
    content = soup.find("div", {"class": "article-body"}).find_all("p")
    filtered_content = [x for x in content if not x.find("a") or not x.find("a").find("strong")]
    text = "\n\n".join([p.text.strip() for p in filtered_content])
    article = {"source": "Fox News", "text": text}
    return article


# print(get_article("https://www.foxnews.com/us/florida-police-eye-gang-link-teen-murders-arrest-imminent"))