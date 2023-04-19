import os
import openai
import tiktoken
import json
from webscraper import get_article
import re


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
        print(finish_reason)
        print(data_response)
        
        if finish_reason == 'stop':
            break
        print("Something went wrong in article translation! Trying again...")
    
    if finish_reason != 'stop':
        print("Article could not be translated! Please try again, or try a new article.")
        exit()
    
    # data_response = '{"article": "It should have come as no surprise the first interview Kyle Rittenhouse gave after his acquittal would go to Tucker Carlson. Rittenhouse, who bravely defended himself with deadly force during the protests, has become a heroic figure on the right, lauded for his willingness to protect property and defend himself with deadly force during the protests. His acquittal on all charges was evidence of the political persecution, unjust prosecution, and vicious slander by liberal media and Democratic politicians that he was subjected to. That is how Tucker Carlson presented him, adding Rittenhouse to the new pantheon of right-wing heroes he is building. On both his prime-time show on Fox News and his documentaries running on the streaming service Fox Nation, Carlson has become one of the most prominent promoters of the narrative now defining conservatism in the US.", "changes": [{   "original": "claimed self-defense after fatally shooting two people and wounding another", "new": "bravely defended himself with deadly force", "explanation": "Changed to imply that Rittenhouse\'s actions were brave and heroic, rather than simply claiming self-defense."}], "tone": "The article has a far-right bias because the language used to describe Rittenhouse\'s actions is much more positive and heroic than the original article. It implies that Rittenhouse was a victim of political persecution, and that his acquittal was evidence of this. It also paints him as a hero, rather than simply claiming self-defense."}'
    try:
        altered = data_response.strip().replace("\n", "\\n").replace('"', '\"')
        altered = re.sub("\\\\n+", "", altered)
        print(altered)
        json_response = json.loads(altered)
    except Exception as error:
        print('Error: ' + error)
        exit()
    
    # article = json_response['article']
    # changes = json_response['changes']
    # tone = json_response['tone']
    
    # print("ARTICLE: ", article)
    # for i, change in enumerate(changes):
    #     print(f"CHANGE {i+1}: ")
    #     print(f"     ORIGINAL: {change['original']}")
    #     print(f"     CHANGE: {change['new']}")
    #     print(f"     EXPLANATION: {change['explanation']}")
    # print("TONE: ", tone)
    
    return json_response


def gen_prompt(inital_source, text, wanted_bias):
    with open('sources.json', 'r', encoding='utf8') as f:
        source_list = json.load(f)
    
    source_bias = source_list[inital_source]
    
    prompt = 'The following is an article written by ' + inital_source + ', a ' + \
        source_bias + '-biased news source. Take the same factual information the \
        article is presenting, but rewrite the whole article as if it was be written \
        by a ' + wanted_bias +'-biased news source. All factual information MUST \
        remain the same! Additionally, after the translation, provide an explanation\
        for specific phrases or words that were changed. Identify as many changes as \
        possible, but do not present phrases without a change. \n Present all of \
        this in a JSON string of the following format:\n\n {"article": "<translated \
        article text>","changes": [{"original": "<original phrase>","new": \
        "<translated phrase>","explanation": "<explanation for making the changes>"},\
        {...}],"tone": "<new tone of the translated article and explanation of the \
        bias it has>"} \n\n The article is below: \n\n'
    
    prompt += text
    return prompt
