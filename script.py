import os
import openai
import tiktoken


class Params():
    MODEL = "text-davinci-003"
    TEMPERATURE = 0.0

def main():
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.organization = os.getenv("OPENAI_ORG_KEY")
    
    prompt = gen_prompt()
    
    enc = tiktoken.encoding_for_model("text-davinci-003")
    max_tokens = 4000 - len(enc.encode(prompt))
    print(max_tokens)

    response = openai.Completion.create(model=Params.MODEL,
                                        # prompt="Say this is a test.",
                                        prompt=prompt,
                                        temperature=Params.TEMPERATURE,
                                        max_tokens=max_tokens)
    print(response.choices[0].text)
    return 0


def gen_prompt():
    source = input("Article source: ")
    prompt = f"The following is an article written by {source}. Please take \
                the same basic information the article is presenting, but \
                turn it into an article that would be written by "
    if source == 'CNN':
        prompt += "Fox News: \n"
    else:
        prompt += "CNN: \n"
    
    article = input("Please copy and paste the article text: ")
    
    prompt += article
    return prompt


if __name__ == '__main__':
    main()
