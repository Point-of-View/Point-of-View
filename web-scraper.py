import requests
from bs4 import BeautifulSoup

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

def get_article(url):
    if not ("cnn.com" in url or "foxnews.com" in url):
        return "Must be a Fox or CNN article"
    
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    if "cnn.com" in url:
        return get_cnn_article(soup)
    elif "foxnews.com" in url:
        return get_fox_article(soup)


def get_cnn_article(soup):
    article = {}
    content = soup.find_all("p", {"class:", "paragraph"})
    article["content"] = "\n\n".join([p.text.strip() for p in content])
    return article

def get_fox_article(soup):
    article = {}
    content = soup.find("div", {"class": "article-body"}).find_all("p")
    article["content"] = "\n\n".join([p.text.strip() for p in content])
    return article

output = get_article("https://www.foxnews.com/us/florida-police-eye-gang-link-teen-murders-arrest-imminent")
print(output)