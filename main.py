import string
import json
import nltk
from nltk.stem import PorterStemmer
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

ps = PorterStemmer()
fp = open("reddit_jokes.json","r",1)

jayson = json.load(fp)

print(len(jayson)) # 194553 reddit jokes
#print(jayson[2]) # first not racist joke

mytest = jayson[2]

#print(type(mytest))
punctuationList = string.punctuation
body = mytest['body']
jid = mytest['id']
print(f"jid: {jid}")
for punct in punctuationList:
    #print(f"trying to replace {punct}")
    body = body.replace(punct,"")

splitBody = body.split(" ")

count = 0
jokeIndex = {}
for word in splitBody:
    if word.lower() in stop_words:
        print("stopword found")
        count +=1
        continue
    else:
        stemmed = ps.stem(word)
        if stemmed in jokeIndex.keys():
            jokeIndex[stemmed].append(count)
        else:
            jokeIndex[stemmed] = [count]
    #print(f"I:{count}  original: {word}    stemmed: {ps.stem(word)}")
    count += 1

print(jokeIndex)
