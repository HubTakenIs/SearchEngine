import string
import json
import nltk
from nltk.stem import PorterStemmer
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

stop_words = set(stopwords.words('english'))

ps = PorterStemmer()
fp = open("reddit_jokes.json","r",1)

jayson = json.load(fp)

print(len(jayson)) # 194553 reddit jokes
#print(jayson[2]) # first not racist joke

mytest = jayson[2]

#print(type(mytest))

# vocabulary
vocabulary = {}

punctuationList = string.punctuation

def removePunctuation(text):
    for punct in punctuationList:
        #print(f"trying to replace {punct}")
        text = text.replace(punct,"")
    return text


def textToIndex(text):
    splitText = text.split(" ")
    count = 0
    jokeIndex = {}
    for word in splitText:
        if word.lower() in stop_words:
            #print("stopword found")
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
    return jokeIndex


def addIndexToVocabulary(index, jid):
    for term in index:
        if term in vocabulary.keys():
            vocabulary[term][jid] = index[term]
        else:
            vocabulary[term] = {jid:index[term]}

body = mytest['body']

for i in range(0,1000):
    #retrieve joke
    joke = jayson[i]
    jid = joke['id']
    # retrieve text from joke
    title = joke['title']
    body = joke['body']
    # remove punctuation
    title = removePunctuation(title)
    body = removePunctuation(body)
    
    #create each index
    title_index = textToIndex(title)
    body_index = textToIndex(body)

    #addIndexToVocabulary
    addIndexToVocabulary(title_index,jid)
    addIndexToVocabulary(body_index,jid)

# write a dictionary to a file
f = open("output.json","w")
f.write(str(vocabulary))
f.close()


#print(vocabulary)
