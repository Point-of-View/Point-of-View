import os
import openai
import tiktoken
from webscraper import get_article


class Params():
    MODEL = "text-davinci-003"
    TEMPERATURE = 0.0

def translate_article(url):
    # Scrape article text
    article = get_article(url)
    if not article:
        return "Must be a Fox or CNN article"
    
    # Generate prompt
    prompt = gen_prompt(article["source"], article["text"])

    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.organization = os.getenv("OPENAI_ORG_KEY")
    
    enc = tiktoken.encoding_for_model("text-davinci-003")
    max_tokens = 4000 - len(enc.encode(prompt))
    print(max_tokens)

    response = openai.Completion.create(model=Params.MODEL,
                                        # prompt="Say this is a test.",
                                        prompt=prompt,
                                        temperature=Params.TEMPERATURE,
                                        max_tokens=max_tokens)
    
    return response.choices[0].text


def gen_prompt(source, text):
    prompt = f"The following is an article written by {source}. Please take \
                the same basic information the article is presenting, but \
                turn it into an article that would be written by "
    if source == 'CNN':
        prompt += "Fox News: \n"
    else:
        prompt += "CNN: \n"

    
    prompt += text
    return prompt
