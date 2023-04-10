from collections import Counter
import tiktoken
from wordfreq import word_frequency
import nltk
# from matplotlib import pyplot as plt


# We should talk about this -- THIS IMPLEMENTATION IS BY TOKEN
article = "It should have come as no surprise the first interview Kyle Rittenhouse gave after his acquittal would go to Tucker Carlson. Rittenhouse, who claimed self-defense after fatally shooting two people and wounding another during a protest in Kenosha, Wisconsin, has become a heroic figure on the right, lauded for his willingness to defend property and defend himself with deadly force during the protests. But recently, his acquittal on all charges added another layer to his status: now he also became a victim of political persecution, unjustly prosecuted by the state and viciously slandered by liberal media and Democratic politicians. That is how Tucker Carlson presented him, adding Rittenhouse to the new pantheon of right-wing victim-heroes he is building. On both his prime-time show on Fox News and his propaganda documentaries running on the streaming service Fox Nation, Carlson has become one of the most prominent promoters of the narrative now defining conservatism in the US: that right-wing violence is not a problem, that White supremacy is a hoax, and that the real threat to democracy is the Democratic-Party-Deep-State alliance. And at Fox News, where Carlson advances this narrative each night, the network has made clear they’re sticking with Tucker, ensuring his indoctrination lines will be repeated across the network. In the interview with Rittenhouse aired Monday night, Carlson emphasized his belief Rittenhouse was a virtuous young man. During the pre-recorded interview, in which Rittenhouse recalled the shootings in polished detail, Carlson not only underscored the righteousness of the teen’s actions, but showed a soft spot for Rittenhouse himself. He introduced Rittenhouse as “bright, decent, sincere, dutiful, and hardworking… exactly the kind of person you would want many more of in your country.” During the interview, he joked with Rittenhouse about their shared propensity for gaining weight, while during a break, he said to his audience, “What a sweet kid.” Shortly after commenting on the shooter’s sweetness, Carlson offered his viewers a summary of his Rittenhouse narrative: “The picture that emerges is of a working-class kid who sincerely believes in America. His community falls apart, and he tries his best to do the right thing, at a time when almost no one else in the community is trying to do the right thing. But he does. And in return for that, the state, under political pressure, throws him in prison.” Carlson has obviously skipped over a key part of the story — where Rittenhouse killed two people. He does so to underscore his broader message to his audience: this could be you or your child. You, the person who loves your country. You, the person who wants to defend your community. You, the person who believes you’re doing the right thing, even when it requires standing alone. And when you do all these things, you are at risk of being unjustly targeted by politicians and prosecutors and the Deep State. It’s the same argument Carlson made just a few weeks ago on his conspiratorial documentary, “Patriot Purge,” his retelling of the Jan. 6 insurrection at the US Capitol. In it, he presented the insurrectionists as good, patriotic Americans, nonviolent protesters who had been set up by the FBI and other Deep-State forces. He warned a second War on Terror was underway, this time aimed directly at conservatives and Trump supporters. The documentary, which ran on Fox Nation, will be followed in a few weeks by one called “The Trial of Kyle,” drawn from hours of interviews and behind-the-scenes filming during the trial. Though Carlson remains Fox News’s biggest star, not everyone on the network is on board with his conspiratorial vision of vigilante conservatism. Earlier this week, Fox News contributors and Never-Trumpers Jonah Goldberg and Steven Hayes quit the network, citing “Patriot Purge” as their reason. “It traffics in all manner of innuendo and conspiracy theories that I think legitimately could lead to violence,” Goldberg said in an interview with NPR’s David Folkenflik. “That for me, and for Steve, was the last straw.” Their departure comes nearly five years after the network went all in on Donald Trump, replacing Trump skeptics like Megyn Kelly and George Will with some of his most ardent supporters, including Carlson and Laura Ingraham. The network’s Trump boosterism was hard to miss, yet so too was giving up lucrative commentator slots. It took “Patriot Purge” to finally stir their consciences to the point of departure. The network’s leading news anchors, Bret Baier and Chris Wallace, also objected to the documentary, running their complaints all the way up to Lachlan Murdoch, the chair and CEO of Fox Corp., the parent company of Fox News. To no avail: the documentary ran, and Fox continues to show its support not only for Carlson’s programming but for the conspiratorial, violent, racist content its viewers — and many Republican Party voters — seem to desire. And that is a key takeaway for the network’s embrace of Carlson: though he plays a powerful role in stitching together events like the insurrection and the Rittenhouse trial into a coherent narrative of conservative grievance and virtue, the underlying appeal plays on the preferences of the network’s and the party’s conservative base. The right had made Rittenhouse a hero while the bodies of the people he shot were still warm. Carlson is there to tell them not only was Rittenhouse right, but they were right, too."

enc = tiktoken.encoding_for_model("text-davinci-003")
tokening = enc.encode(article)

total_article_len = len(tokening)
token_counts = Counter(tokening)
most_common_tokens = [key for key, _ in token_counts.most_common(20)]
most_common_words = enc.decode(most_common_tokens)
least_common_tokens = [key for key, _ in token_counts.most_common()[-20:]]
least_common_words = enc.decode(least_common_tokens)

print(most_common_tokens)
print(most_common_words)
print(least_common_tokens)
print(least_common_words)

# for word in most_common_words:
#     print(word_frequency(word, 'en'))
nltk.download('brown')
corpus = nltk.corpus.brown.words()
# This next line is an issue -- it's doing word by word, without spaces
corpus_tokenized = [enc.encode(text) for text in corpus]
full_corpus_token = [item for sublist in corpus_tokenized for item in sublist]
total_corpus_len = len(full_corpus_token)
# print(total_corpus_len)
# print(full_corpus_token[:20])
corpus_counts = Counter(full_corpus_token)

most_common_corpus_tokens = [key for key, _ in corpus_counts.most_common(20)]
most_common_corpus_words = enc.decode(most_common_corpus_tokens)
least_common_corpus_tokens = [key for key, _ in corpus_counts.most_common()[-20:]]
least_common_corpus_words = enc.decode(least_common_corpus_tokens)

print(most_common_corpus_tokens)
print(most_common_corpus_words)
print(least_common_corpus_tokens)
print(least_common_corpus_words)

# token_freqs = dict.fromkeys(most_common_tokens, -1)
# for token in most_common_tokens:
#     # THIS DOESNT WORK I WAS CONFUSED I AM CONFUSED LETS TALK LOL
#     article_freq = token_counts[token] / total_article_len
#     corpus_freq = full_corpus_token[token] / total_corpus_len
    
#     old_min = 0.00000066
#     old_max = 0.04156
#     new_min = -2
#     new_max = 2

#     raw_value = article_freq/corpus_freq
#     clipped_value = max(min(raw_value, old_max), old_min)
#     scaled_value = ((clipped_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
#     token_freqs[token] = scaled_value

# print(token_freqs)

# TODO: Exclude "filler tokens" -- any sort of punctuation (commas, periods, etc), and filler words (a, the, etc)
# This can be done by looking at the token list/tokenizer, they should be early on, so shouldn't be too hard
