import tiktoken

enc = tiktoken.encoding_for_model("text-davinci-003")

tokens = set()

for thing in ["TITLE: ", "CHANGES: ", "[{", "{ORIGINAL: ", "ORIGNAL: ", "NEW: ", "EXPLANATION: ", "},", "}]", "TONE: "]:
    for elem in enc.encode(thing):
        tokens.add(elem)
        print(enc.decode([elem]))
    
print(tokens)
