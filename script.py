import os
import openai


def main():
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=get_prompt(),
                                        temperature=0,
                                        max_tokens=7)
    print(response)
    return 0


def get_prompt():
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
