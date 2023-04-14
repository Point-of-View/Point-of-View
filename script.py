import os
import openai
import tiktoken
import json


class Params():
    MODEL = "text-davinci-003"
    TEMPERATURE = 0.2

def main():
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        openai.organization = os.getenv("OPENAI_ORG_KEY")
    except Exception as e:
        print(f"Error loading OpenAI organization: {e} \nMoving on...")
    
    source = input("Article source: ")
    wanted_bias = input("Wanted translation bias: ")
    prompt = gen_prompt(source, wanted_bias)
    
    enc = tiktoken.encoding_for_model("text-davinci-003")
    max_tokens = 4000 - len(enc.encode(prompt))
    # print(max_tokens)

    response = openai.Completion.create(model=Params.MODEL,
                                        prompt=prompt,
                                        temperature=Params.TEMPERATURE,
                                        max_tokens=max_tokens)
    
    data_response = response.choices[0].text
    # print(data_response)
    
    # data_response = '{"article": "It should have come as no surprise the first interview Kyle Rittenhouse gave after his acquittal would go to Tucker Carlson. Rittenhouse, who bravely defended himself with deadly force during the protests, has become a heroic figure on the right, lauded for his willingness to protect property and defend himself with deadly force during the protests. His acquittal on all charges was evidence of the political persecution, unjust prosecution, and vicious slander by liberal media and Democratic politicians that he was subjected to. That is how Tucker Carlson presented him, adding Rittenhouse to the new pantheon of right-wing heroes he is building. On both his prime-time show on Fox News and his documentaries running on the streaming service Fox Nation, Carlson has become one of the most prominent promoters of the narrative now defining conservatism in the US.", "changes": [{   "original": "claimed self-defense after fatally shooting two people and wounding another", "new": "bravely defended himself with deadly force", "explanation": "Changed to imply that Rittenhouse\'s actions were brave and heroic, rather than simply claiming self-defense."}], "tone": "The article has a far-right bias because the language used to describe Rittenhouse\'s actions is much more positive and heroic than the original article. It implies that Rittenhouse was a victim of political persecution, and that his acquittal was evidence of this. It also paints him as a hero, rather than simply claiming self-defense."}'
    json_response = json.loads(data_response)
    
    article = json_response['article']
    changes = json_response['changes']
    tone = json_response['tone']
    
    print("ARTICLE: ", article)
    for i, change in enumerate(changes):
        print(f"CHANGE {i+1}: ")
        print(f"     ORIGINAL: {change['original']}")
        print(f"     CHANGE: {change['new']}")
        print(f"     EXPLANATION: {change['explanation']}")
    print("TONE: ", tone)
    
    return 0


def gen_prompt(inital_source, wanted_bias):
    with open('sources.json', 'r', encoding='utf8') as f:
        source_list = json.load(f)
    
    source_bias = source_list[inital_source]
    
    prompt = f'The following is an article written by {inital_source}, a {source_bias} news source. Please take \
                the same basic information the article is presenting, but \
                turn it into an article that would be written by a {wanted_bias} news source. Additionally, \
                after your translation, provide an explanation for specific phrases or words you \
                changed, or any reasonings you had for making any and all changes you did. \n\n Present all of this in \
                a JSON string, where the translated article has the key "article". The phrases changed will \
                be a list with the key "changes" and within the list, each phrase will have the original phrase \
                (key "original"), the changed phrase (key "new") and the explanation (key "explanation").\
                Additionally, have one last JSON field explaining the new tone of the article (key "tone"), and why \
                it has the bias that it does. \
                \n\n The article is below: \n\n'
    
    article = input("Please copy and paste the article text: ")
    
    prompt += article
    return prompt


if __name__ == '__main__':
    main()
