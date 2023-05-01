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


far_left_token_dict = Counter(far_left_tokening)
liberal_token_dict = Counter(liberal_tokening)
moderate_token_dict = Counter(moderate_tokening)
conservative_token_dict = Counter(conservative_tokening)
far_right_token_dict = Counter(far_right_tokening)


far_left_total = sum(far_left_token_dict.values())
liberal_total = sum(liberal_token_dict.values())
moderate_total = sum(moderate_token_dict.values())
conservative_total = sum(conservative_token_dict.values())
far_right_token_dict = sum(far_right_token_dict.values())


far_left_scores = {}


for token, count in far_left_token_dict.items():
    far_left_scores[str(token)] = count / far_left_total
with open('far_left.json', 'w', encoding='utf-8') as f:
    json.dump(far_left_scores, f)
