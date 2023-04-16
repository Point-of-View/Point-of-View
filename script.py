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
    except Exception as e:
        print("Something went wrong in the response! Rerunning the translation..")
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
    
    article = input("Please copy and paste the article text: ")
    # article = "It should have come as no surprise the first interview Kyle Rittenhouse gave after his acquittal would go to Tucker Carlson. Rittenhouse, who claimed self-defense after fatally shooting two people and wounding another during a protest in Kenosha, Wisconsin, has become a heroic figure on the right, lauded for his willingness to defend property and defend himself with deadly force during the protests. But recently, his acquittal on all charges added another layer to his status: now he also became a victim of political persecution, unjustly prosecuted by the state and viciously slandered by liberal media and Democratic politicians. That is how Tucker Carlson presented him, adding Rittenhouse to the new pantheon of right-wing victim-heroes he is building. On both his prime-time show on Fox News and his propaganda documentaries running on the streaming service Fox Nation, Carlson has become one of the most prominent promoters of the narrative now defining conservatism in the US: that right-wing violence is not a problem, that White supremacy is a hoax, and that the real threat to democracy is the Democratic-Party-Deep-State alliance. And at Fox News, where Carlson advances this narrative each night, the network has made clear they’re sticking with Tucker, ensuring his indoctrination lines will be repeated across the network. In the interview with Rittenhouse aired Monday night, Carlson emphasized his belief Rittenhouse was a virtuous young man. During the pre-recorded interview, in which Rittenhouse recalled the shootings in polished detail, Carlson not only underscored the righteousness of the teen’s actions, but showed a soft spot for Rittenhouse himself. He introduced Rittenhouse as “bright, decent, sincere, dutiful, and hardworking… exactly the kind of person you would want many more of in your country.” During the interview, he joked with Rittenhouse about their shared propensity for gaining weight, while during a break, he said to his audience, “What a sweet kid.” Shortly after commenting on the shooter’s sweetness, Carlson offered his viewers a summary of his Rittenhouse narrative: “The picture that emerges is of a working-class kid who sincerely believes in America. His community falls apart, and he tries his best to do the right thing, at a time when almost no one else in the community is trying to do the right thing. But he does. And in return for that, the state, under political pressure, throws him in prison.” Carlson has obviously skipped over a key part of the story — where Rittenhouse killed two people. He does so to underscore his broader message to his audience: this could be you or your child. You, the person who loves your country. You, the person who wants to defend your community. You, the person who believes you’re doing the right thing, even when it requires standing alone. And when you do all these things, you are at risk of being unjustly targeted by politicians and prosecutors and the Deep State. It’s the same argument Carlson made just a few weeks ago on his conspiratorial documentary, “Patriot Purge,” his retelling of the Jan. 6 insurrection at the US Capitol. In it, he presented the insurrectionists as good, patriotic Americans, nonviolent protesters who had been set up by the FBI and other Deep-State forces. He warned a second War on Terror was underway, this time aimed directly at conservatives and Trump supporters. The documentary, which ran on Fox Nation, will be followed in a few weeks by one called “The Trial of Kyle,” drawn from hours of interviews and behind-the-scenes filming during the trial. Though Carlson remains Fox News’s biggest star, not everyone on the network is on board with his conspiratorial vision of vigilante conservatism. Earlier this week, Fox News contributors and Never-Trumpers Jonah Goldberg and Steven Hayes quit the network, citing “Patriot Purge” as their reason. “It traffics in all manner of innuendo and conspiracy theories that I think legitimately could lead to violence,” Goldberg said in an interview with NPR’s David Folkenflik. “That for me, and for Steve, was the last straw.” Their departure comes nearly five years after the network went all in on Donald Trump, replacing Trump skeptics like Megyn Kelly and George Will with some of his most ardent supporters, including Carlson and Laura Ingraham. The network’s Trump boosterism was hard to miss, yet so too was giving up lucrative commentator slots. It took “Patriot Purge” to finally stir their consciences to the point of departure. The network’s leading news anchors, Bret Baier and Chris Wallace, also objected to the documentary, running their complaints all the way up to Lachlan Murdoch, the chair and CEO of Fox Corp., the parent company of Fox News. To no avail: the documentary ran, and Fox continues to show its support not only for Carlson’s programming but for the conspiratorial, violent, racist content its viewers — and many Republican Party voters — seem to desire. And that is a key takeaway for the network’s embrace of Carlson: though he plays a powerful role in stitching together events like the insurrection and the Rittenhouse trial into a coherent narrative of conservative grievance and virtue, the underlying appeal plays on the preferences of the network’s and the party’s conservative base. The right had made Rittenhouse a hero while the bodies of the people he shot were still warm. Carlson is there to tell them not only was Rittenhouse right, but they were right, too."

    
    prompt += article
    return prompt


if __name__ == '__main__':
    main()
