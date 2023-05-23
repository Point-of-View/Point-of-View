import tiktoken


# Get the tokens for the key words in the prompt/returned text for parsing

enc = tiktoken.encoding_for_model("text-davinci-003")

tokens = set()

# Tokenize the key words
for thing in ["TITLE: ", "CHANGES: ", "[{", "{ORIGINAL: ", "ORIGNAL: ", "NEW: ", "EXPLANATION: ", "},", "}]", "TONE: "]:
    for elem in enc.encode(thing):
        tokens.add(elem)
        print(enc.decode([elem]))
    
print(tokens)
