import os
import openai
import tiktoken
import json
from webscraper import get_article
import re
import ast


class Params():
    MODEL = "text-davinci-003"
    TEMPERATURE = 0.5

def translate_article(url, wanted_bias):
    # Scrape article text
    article = get_article(url)
    if not article:
        return "Must be a Fox or CNN article"
    
    # Generate prompt
    prompt = gen_prompt(article["source"], article["text"], wanted_bias)

    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        openai.organization = os.getenv("OPENAI_ORG_KEY")
    except Exception as e:
        print(f"Error loading OpenAI organization: {e} \nMoving on...")
    
    enc = tiktoken.encoding_for_model("text-davinci-003")
    tokens_left = 4096 - len(enc.encode(prompt))
    print(tokens_left)
    if tokens_left < 2250:
        print("We're sorry! This article is too long to translate at this time. Please try a different article.")
        exit()
    
    finish_reason = ""
    
    for _ in range(3):
        response = openai.Completion.create(model=Params.MODEL,
                                            prompt=prompt,
                                            temperature=Params.TEMPERATURE,
                                            max_tokens=tokens_left)
        
        data_response = response.choices[0].text
        finish_reason = response.choices[0].finish_reason
        
        if finish_reason == 'stop':
            break
        print("Something went wrong in article translation! Trying again...")
    
    if finish_reason != 'stop':
        print("Article could not be translated! Please try again, or try a new article.")
        exit()
    
    try:
        # print(data_response)
        # altered = data_response.strip().replace("\n", "\\n").replace('"', '\"')
        altered = data_response.strip()
        print(altered)
        
        title = re.search(r"(?i)TITLE:\s*(.*)\s*ARTICLE:", altered, re.DOTALL).group(1)
        print("TITLE ", title)
        article = re.search(r"(?i)ARTICLE:\s*(.*)\s*CHANGES:", altered, re.DOTALL).group(1)
        print("ARTICLE ", article)
        # changes = re.findall(r"\{ORIGINAL:\s*'(.*)'\s*NEW:\s*'(.*)'\s*EXPLANATION:\s*(.*)\}", altered, re.DOTALL)
        # changes = re.findall(r"\{ORIGINAL:\s*'(.*)'\s*NEW:\s*'(.*)'\s*EXPLANATION:\s*(.*?)'\}", altered, re.DOTALL)
        # changes = re.findall(r"{ORIGINAL:\s*'([^']*)'\s*NEW:\s*'([^']*)'\s*EXPLANATION:\s*'([^']*)'}", altered, re.DOTALL)
        # changes = re.findall(r"CHANGES:\s*\[({[^{}]*\n*[^{}]*})+\]", altered, re.DOTALL)
        # changes = re.findall(r"{ORIGINAL:\s*'([^']*)'\s*NEW:\s*'([^']*)'\s*EXPLANATION:\s*([^}]*)}", altered, re.DOTALL)
        # changes = re.search(r"(?i)CHANGES:\s*(.*)\s*TONE:", altered, re.DOTALL).group(1)
        changes = re.search(r"(?<=\[).*?(?=\])", altered, re.DOTALL).group(0)
        changes = changes.replace('"', '\"')
        # changes = '[' + changes + ']'
        print(changes)
        try:
            change_list = ast.literal_eval(changes)
        except Exception as e:
            print(f"Something went wrong in parsing the changes: {e}")
            change_list = []
        print("CHANGES" , change_list)
        tone = re.search(r"(?i)TONE:\s*(.*)", altered, re.DOTALL).group(1)
        print("TONE ", tone)
        # altered = data_response.strip().replace("\n", "<p>").replace('"', '\"')
        # json_response = json.loads(altered)
    except Exception as error:
        print(f'Error: {error}')
        exit()

    return title, article, changes, tone


def gen_prompt(inital_source, text, wanted_bias):
    with open('sources.json', 'r', encoding='utf8') as f:
        source_list = json.load(f)
    
    source_bias = source_list["news_bias"][inital_source]
    example_sources = ', '.join(source_list["examples"][wanted_bias]["sources"])
    example_journalists = ', '.join(source_list["examples"][wanted_bias]["journalists"])
    
    prompt = 'The following is an article written by ' + inital_source + ', a ' + source_bias + '-biased news source. Take the same factual information the article is presenting, but rewrite the whole article as if it was be written by a ' + wanted_bias +'-biased news source, such as ' + example_sources
    
    if wanted_bias != "moderate":
        prompt +=', or written by ' + wanted_bias + ' journalists, such as ' + example_journalists
    
    prompt += ". All factual information MUST remain the same, and be as sincere and journalistic as possible. Additionally, after the translation, provide an explanation for specific phrases or words that were changed. Identify as many changes as possible, but do not present phrases without a change.\nPresent all of this in the following text format:\n\nTITLE: <new article title> ARTICLE: <translated article text> CHANGES: [{ORIGINAL: <original phrase> NEW: <new phrase> EXPLANATION: <explanation for making the changes>}, {ORIGINAL: ...}, {...}] TONE: <new tone of the translated article and explanation of the bias it has>\n\nThe article is below:\n\n"
    
    prompt += text
    return prompt




translate_article("https://www.foxnews.com/us/florida-police-eye-gang-link-teen-murders-arrest-imminent", 'far-left')