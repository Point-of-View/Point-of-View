import json
import os
import re

import openai
import tiktoken

from webscraper import get_article


class Params():
    """
    Basic parameters for the OpenAI model
    """
    MODEL = "text-davinci-003"
    TEMPERATURE = 0.5

def translate_article(url, wanted_bias):
    """
    Performs the main backend article translation

    :param url: Original article url
    :type url: string
    :param wanted_bias: Bias for article to be translated into
    :type wanted_bias: string
    :return: Dictionary containing key pieces of translation -- title, article, changes, tone
    :rtype: dict
    """
    
    # Scrape article text
    article = get_article(url)
    if not article:
        return "Must be a Fox or CNN article"
    
    # Generate prompt
    changes_prompt = gen_changes(article["source"], article["text"], wanted_bias)

    # Load your API key
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.organization = os.getenv("OPENAI_ORG_KEY")
    
    # Get token counts, exit if not enough remaining for a response
    enc = tiktoken.encoding_for_model(Params.MODEL)
    tokens_left = 4080 - len(enc.encode(changes_prompt))
    print(tokens_left)
    if tokens_left < 2250:
        print("We're sorry! This article is too long to translate at this time. Please try a different article.")
        exit()
    
    finish_reason = ""
    
    # Perform API call. Try up to three times if it doesn't work initially
    for _ in range(3):
        response = openai.Completion.create(model=Params.MODEL,
                                            prompt=changes_prompt,
                                            temperature=Params.TEMPERATURE,
                                            max_tokens=tokens_left,
                                            logit_bias = json.load(open(f'word_scores/{wanted_bias}_scores.json', 'r', encoding='utf8'))
                                            )
                
        data_response = response.choices[0].text
        finish_reason = response.choices[0].finish_reason
        
        if finish_reason == 'stop':
            break
        print("Something went wrong in article translation! Trying again...")
    
    # If, after three interations, the call still fails, exit
    if finish_reason != 'stop':
        print("Article could not be translated! Please try again, or try a new article.")
        exit()
    
    try:
        # Escape characters in response
        altered = data_response.strip().replace("\n", "\\n").replace('"', '\"').replace("'", "\'")
        
        # Find the title in the response
        title = re.search(r"(?i)TITLE:\s*(.*)\s*CHANGES:", altered, re.DOTALL).group(1) if re.search(r"(?i)TITLE:\s*(.*)\s*CHANGES:", altered, re.DOTALL) else ""
        
        # Find the changes in the response
        changes = re.search(r"(?i)CHANGES:\s*(.*)\s*TONE:", altered, re.DOTALL).group(1) if re.search(r"(?i)CHANGES:\s*(.*)\s*TONE:", altered, re.DOTALL) else ""
        originals = re.findall(r"(?i)ORIGINAL:\s*(.*?)\s*NEW:", changes, re.DOTALL)
        news = re.findall(r"(?i)NEW:\s*(.*?)\s*EXPLANATION:", changes, re.DOTALL)
        explanations = re.findall(r"(?i)EXPLANATION:\s*(.*?)\s*}", changes, re.DOTALL)

        if len(originals) != len(news) != len(explanations):
            print("ERROR GETTING CHANGES!! Please try again.")
            exit()
        
        num_changes = len(originals)
        change_list = [None] * num_changes
        
        for i in range(num_changes):
            change_list[i] = (originals[i], news[i], explanations[i])
        
        # Find the changes in the response
        tone = re.search(r"(?i)TONE:\s*(.*)", altered, re.DOTALL).group(1)
    
    except Exception as error:
        print(f'Error parsing response: {error}')
        exit()
    
    # Place the generated changes into the article
    changed_article = replace_changes(article["text"], change_list)
    
    return {"TITLE": title, "ARTICLE": changed_article, "CHANGES": change_list, "TONE": tone}


def gen_changes(inital_source, text, wanted_bias):
    """
    Generate the prompt to pass to text-davinci-003

    :param inital_source: Where the original article is from
    :type inital_source: string
    :param text: Original article's text
    :type text: string
    :param wanted_bias: Bias for article to be translated into
    :type wanted_bias: string
    :return: Full prompt to pass into the OpenAI model
    :rtype: string
    """
    
    # Load list of sources and journalists by bias
    with open('sources.json', 'r', encoding='utf8') as f:
        source_list = json.load(f)
    
    # Get the example sources and journalists
    source_bias = source_list["news_bias"][inital_source]
    example_sources = ', '.join(source_list["examples"][wanted_bias]["sources"])
    example_journalists = ', '.join(source_list["examples"][wanted_bias]["journalists"])
    
    # First part of the prompt
    prompt = 'The following is an article written by ' + inital_source + ', a ' + source_bias + '-biased news source. Create many phrase changes as if it was an opinion piece written by a ' + wanted_bias +'-biased news source, such as ' + example_sources
    
    # Append journalist names to prompt, for all biases except moderate
    if wanted_bias != "moderate":
        prompt +=', or written by ' + wanted_bias + ' journalists, such as ' + example_journalists
    
    # Finish prompt
    prompt += ". Identify as many changes as possible, but do not present phrases without a change. Make sure changes are in the correct bias. Do not change facts. For each change, present the original phrase, the new phrase, and an explanation for the change. Also, create a title for the new article, and an explanation of the new tone of the article. Present it in the following format: TITLE: <new article title> CHANGES: [{ORIGINAL: <original phrase> NEW: <new phrase> EXPLANATION: <explanation for making the changes>}, {ORIGINAL: ...}, {...}] TONE: <new tone of the translated article and explanation of the bias it has>\n\nThe article is below:\n\n"
    
    # Append actual article text into prompt and return
    prompt += text
    return prompt


def replace_changes(article, change_list):
    """
    Place the generated changes into the new article

    :param article: Text of the original article
    :type article: string
    :param change_list: All of the changes to be made, containing the original text, new text, and explanation
    :type change_list: list
    :return: The new article, with changes placed in
    :rtype: string
    """
    for orig, new, expl in change_list:
        article = article.replace(orig, new)
    return article
