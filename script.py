import os
import openai
import tiktoken
import json


class Params():
    MODEL = "text-davinci-003"
    TEMPERATURE = 0.5

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
    print(max_tokens)

    response = openai.Completion.create(model=Params.MODEL,
                                        prompt=prompt,
                                        temperature=Params.TEMPERATURE,
                                        max_tokens=max_tokens)
    
    data_response = response.choices[0].text
    print(data_response)
    
    # data_response = '{"article": "It should have come as no surprise the first interview Kyle Rittenhouse gave after his acquittal would go to Tucker Carlson. Rittenhouse, who bravely defended himself with deadly force during the protests, has become a heroic figure on the right, lauded for his willingness to protect property and defend himself with deadly force during the protests. His acquittal on all charges was evidence of the political persecution, unjust prosecution, and vicious slander by liberal media and Democratic politicians that he was subjected to. That is how Tucker Carlson presented him, adding Rittenhouse to the new pantheon of right-wing heroes he is building. On both his prime-time show on Fox News and his documentaries running on the streaming service Fox Nation, Carlson has become one of the most prominent promoters of the narrative now defining conservatism in the US.", "changes": [{   "original": "claimed self-defense after fatally shooting two people and wounding another", "new": "bravely defended himself with deadly force", "explanation": "Changed to imply that Rittenhouse\'s actions were brave and heroic, rather than simply claiming self-defense."}], "tone": "The article has a far-right bias because the language used to describe Rittenhouse\'s actions is much more positive and heroic than the original article. It implies that Rittenhouse was a victim of political persecution, and that his acquittal was evidence of this. It also paints him as a hero, rather than simply claiming self-defense."}'
    try:
        json_response = json.loads(data_response)
    except Exception as error:
        print(f"Something went wrong in the response! Error: {error}")
        print("Rerunning the translation..")
        response = openai.Completion.create(model=Params.MODEL,
                                        prompt=prompt,
                                        temperature=Params.TEMPERATURE,
                                        max_tokens=max_tokens)
        data_response = response.choices[0].text
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
    
    prompt = f'The following is an article written by {inital_source}, a {source_bias}-biased news source. Take \
                the same basic information the article is presenting, but rewrite the whole article as if \
                it was be written by a {wanted_bias}-biased news source. Additionally, \
                after the translation, provide an explanation for specific phrases or words that were \
                changed, or any reasonings made for making any and all changes. Identify \
                as many changes as possible. \n\n Present all of this in a JSON string, where the translated \
                article has the key "article". The phrases changed will be a list (key "changes") and \
                within the list, each phrase will have the original phrase (key "original"), the changed \
                phrase (key "new") and the explanation (key "explanation"). \
                Additionally, have one last JSON field explaining the new tone of the article (key "tone"), and why \
                it has the bias that it does. \
                \n\n The article is below: \n\n'
    
    # article = input("Please copy and paste the article text: ")
    article = "President Joe Biden’s public pronouncements about the war in Ukraine ring hollow in light of the recently leaked intelligence documents. Congress and the American people must demand accountability, truth and not more lies before we are led into another war or something much worse. Unfortunately, the mainstream media have twisted the story about the allegation that a 21-year-old National Guardsman leaked finished intelligence products on gaming internet sites. \
        They myopically focus on the leaker, his crime and not on the substance of the leaked material in order to protect President Joe Biden. However, we need to ask whether the president is lying about our role in the war in Ukraine, which could have grave consequences for us all. The fact is historically presidents lie to the American people about wars. President Franklin D. Roosevelt in 1940 lied to Americans that \"Your boys are not going to be sent into any foreign wars.\" Besides, at that time we were providing lethal aid to the United Kingdom. We went to war after Japan attacked Pearl Harbor in December 1941. President Lyndon B. Johnson lied about the threat posed by the North Vietnamese to preserve his political power. \
            In 1964 Johnson told an Akron, Ohio election campaign crowd, \"We are not about to send American boys nine or 10 thousand miles away from home to do what Asian boys ought to be doing for themselves.\" Then after being elected, LBJ sent U.S. combat troops to the jungles of Vietnam, lying to the American people about the attack on US forces in the Gulf of Tonkin, eventually deploying half a million personnel until our withdrawal in 1975 with our tail tucked and at the cost of more than 58,000 American lives. President George W. Bush lied about the reason we invaded Iraq to eliminate weapons of mass destruction. Before the war, CIA Director George Tenet warned Bush not to use sketchy intelligence about Iraq.  \
                Bush knew Saddam Hussein no longer had an arsenal of WMD and yet the president misled the American people, and after the 2003 invasion, officials confirmed Iraq had abandoned its programs years earlier. Other presidents in our history lied to the American people about war: James Polk lied about Mexico invading the US which led to the Mexican-American War because he wanted to add Texas as another slave state. William McKinley lied that the Spanish had blown up the USS Maine warship in Havana Harbor, which led to the Spanish-American War. It could be President Biden is lying about our role in the Ukraine war much as past presidents lied.  Certainly, some of the leaked intelligence suggests the war in Ukraine isn’t going as swimmingly as Biden and his administration have suggested. \
                    Unfortunately, Biden’s apologists in the mainstream media focus on the leaker. That’s really only a small part of the broader story. If in fact the young Airman arrested is found guilty of leaking, he will pay a price.  However, the real story is the content of the material shared across the internet. Does it paint a different story than what the Biden administration has told the American people? Is President Biden lying to the American people and if so, why? The fact is many, if not most, of the products shared about the Ukraine war are finished intelligence reports, which paint a very different picture from that which the Biden administration broadcasts. We should ask: What’s the truth? Is America more directly involved in the Ukraine war than previously reported? \
                        Are American troops fighting Russians? Is the Biden administration purposely draining our weapons arsenals to favor the Chinese? Can Ukraine really win the war against giant Russia? There are so many questions left unanswered. My point is simple. The story about a young Airman leaking finished intelligence products is serious. The Pentagon will address that issue to protect our methods and sources. However, the more significant issue is whether President Biden and his proxies are telling the American people the truth about the Ukraine war. After all, Biden has never explained our national interests in that war other than to acknowledge we’re helping to protect Ukrainian 'democracy' and to keep the Russians from gobbling up more of Europe. Last year, President Biden soberly promised at a NATO summit \"We are going to stick with Ukraine … as long as it takes to in fact make sure that they are not defeated … by Russia.\"  That sounds too much like LBJ and the Vietnam war. The leaked intelligence documents sound an alarm bell regarding America’s role in the Ukraine war.  It’s past time President Biden level with the American people about our interests and whether our continued role in that war could escalate into something much worse."

    prompt += article
    return prompt


if __name__ == '__main__':
    main()
