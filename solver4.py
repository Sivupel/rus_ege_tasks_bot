import spacy
import pickle

ru_nlp = spacy.load('ru_core_news_md')

def load():
   
    with open(file="accent.dat", mode='rb') as f:
        accent = pickle.loads(f.read())
    return  accent

accent = load()
  

def tokenize(text, accent):
    res = []
    doc = ru_nlp(text)
    for token in doc:
        word = {"token": token.text}
        if word["token"] in accent:
            word["interpretations"] = accent[word["token"]]
        if word["token"].lower() in accent:
            word["interpretations"] = accent[word["token"].lower()]
        word["whitespace"] = token.whitespace_
        res.append(word)
    return res

def accentuate(word):
    if  (not "interpretations" in word):
        return word["token"]
    else:
        res = accentuation(word["interpretations"])
        if not (res is None):
            return res
    

def accentuation(interpretations):
    if len(interpretations) == 0:
        return None
    res = interpretations[0]["accentuated"]
    for i in range(1, len(interpretations)):
        if interpretations[i]["accentuated"] != res:
            return None
    return res

def fin(text, accent):
    res = ""
    words = tokenize(text, accent)
    for i in range(len(words)):
        accentuated = accentuate(words[i])
        res += accentuated
        res += words[i]["whitespace"]
    return res
       
res = fin(text, accent)    

f = open("in.txt", mode='r', encoding='utf-8')
text = f.read()
f.close()


f = open("out.txt", mode='w', encoding='utf-8')
f.write(res)
f.close()
