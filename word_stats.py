import tiktoken
from collections import Counter
import json


FL = 0
L = 1
M = 2
C = 3
FR = 4


def load_texts():
    with open('article_texts/far_left.txt', 'r', encoding='utf-8') as f:
        far_left_text = f.read()
    f.close()

    with open('article_texts/liberal.txt', 'r', encoding='utf-8') as f:
        liberal_text = f.read()
    f.close()

    with open('article_texts/moderate.txt', 'r', encoding='utf-8') as f:
        moderate_text = f.read()
    f.close()

    with open('article_texts/conservative.txt', 'r', encoding='utf-8') as f:
        conservative_text = f.read()
    f.close()

    with open('article_texts/far_right.txt', 'r', encoding='utf-8') as f:
        far_right_text = f.read()
    f.close()

    return far_left_text, liberal_text, moderate_text, conservative_text, far_right_text


enc = tiktoken.encoding_for_model("text-davinci-003")


corpus = load_texts()


far_left_tokening = enc.encode(corpus[FL])
liberal_tokening = enc.encode(corpus[L])
moderate_tokening = enc.encode(corpus[M])
conservative_tokening = enc.encode(corpus[C])
far_right_tokening = enc.encode(corpus[FR])

far_left_total = len(far_left_tokening)
liberal_total = len(liberal_tokening)
moderate_total = len(moderate_tokening)
conservative_total = len(conservative_tokening)
far_right_total = len(far_right_tokening)


far_left_token_dict = Counter(far_left_tokening).most_common(300)
liberal_token_dict = Counter(liberal_tokening).most_common(300)
moderate_token_dict = Counter(moderate_tokening).most_common(300)
conservative_token_dict = Counter(conservative_tokening).most_common(300)
far_right_token_dict = Counter(far_right_tokening).most_common(300)


far_left_scores = {}
liberal_scores = {}
moderate_scores = {}
conservative_scores = {}
far_right_scores = {}


for token, count in far_left_token_dict:
    far_left_scores[str(token)] = count / far_left_total
with open('article_scores/far_left.json', 'w', encoding='utf-8') as f:
    json.dump(far_left_scores, f)

for token, count in liberal_token_dict:
    liberal_scores[str(token)] = count / liberal_total
with open('article_scores/liberal.json', 'w', encoding='utf-8') as f:
    json.dump(liberal_scores, f)

for token, count in moderate_token_dict:
    moderate_scores[str(token)] = count / moderate_total
with open('article_scores/moderate.json', 'w', encoding='utf-8') as f:
    json.dump(moderate_scores, f)

for token, count in conservative_token_dict:
    conservative_scores[str(token)] = count / conservative_total
with open('article_scores/conservative.json', 'w', encoding='utf-8') as f:
    json.dump(conservative_scores, f)

for token, count in far_right_token_dict:
    far_right_scores[str(token)] = count / far_right_total
with open('article_scores/far_right.json', 'w', encoding='utf-8') as f:
    json.dump(far_right_scores, f)
