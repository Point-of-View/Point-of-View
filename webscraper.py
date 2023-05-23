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
    """
    Gets the text of the wanted article

    :param url: Article url of interests
    :type url: string
    :return: Dictionary of scraped information
    :rtype: dict
    """
    
    # Only functional with CNN and Fox currently
    if not ("cnn.com" in url or "foxnews.com" in url):
        return
    
    # Set up Requests and Beautiful Soup
    req = requests.get(url=url, headers=headers, timeout=30)
    soup = BeautifulSoup(req.content, 'html.parser')

    if "cnn.com" in url:
        return get_cnn_article(soup)
    elif "foxnews.com" in url:
        return get_fox_article(soup)


def get_cnn_article(soup):
    """
    Perform scraping for CNN articles

    :param soup: BeautifulSoup
    :type soup: BeautifulSoup object
    :return: Dictionary of scraped information
    :rtype: dict
    """
    
    title = soup.find("h1").text.strip()
    content = soup.find_all("p", {"class:", "paragraph"})
    text = "\n\n".join([p.text.strip() for p in content])
    return {"source": "CNN", "text": text, "title": title}

def get_fox_article(soup):
    """
    Perform scraping for Fox News articles

    :param soup: BeautifulSoup
    :type soup: BeautifulSoup object
    :return: Dictionary of scraped information
    :rtype: dict
    """
    
    title = soup.find("h1").text.strip()
    content = soup.find("div", {"class": "article-body"}).find_all("p")
    filtered_content = [x for x in content if not x.find("a") or not x.find("a").find("strong")]
    text = "\n\n".join([p.text.strip() for p in filtered_content])
    return {"source": "Fox News", "text": text, "title": title}
