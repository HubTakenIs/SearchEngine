import string
import json
import nltk
import re
nltk.download('stopwords')
nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

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
    text = text.replace("\n"," ")
    text = text.replace('“',' ')
    text = text.replace('”',' ')
    text = text.replace('’',' ')
    text = text.replace('‘',' ')


    return text


def textToIndex(text):
    splitText = word_tokenize(text)
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

<<<<<<< HEAD
for i in range(0,10):
    # set as key of dict
    maindict = {}
    maindict[("term", 1)] = ({"json":"object"},2)
    maindict[("not", 2)] = ({"json":"object"},2)
    print(maindict)
    
=======



for i in range(0,11):
>>>>>>> 6c116d73c17c3f4117c0257d450b859d01b32e90
    #retrieve joke
    joke = jayson[i]
    jid = joke['id']
    # retrieve text from joke
    title = joke['title']
    body = joke['body']
    # remove punctuation
    title = removePunctuation(title)
    body = removePunctuation(body)
<<<<<<< HEAD

    joke_text = title + " " + body

    

    joke_index = textToIndex(joke_text)

    # normalised Term Frequency
    # tf = term occurance / most occuring term
    # tf per document?
    
    # joke index

    addIndexToVocabulary(joke_index,jid)
    
    #print("JOKE INDEX ")
    #print(joke_index)
=======
    joke1 = title + " " + body
    
    #create each index
    joke_index = textToIndex(joke1)
    #addIndexToVocabulary
    addIndexToVocabulary(joke_index,jid)
    
>>>>>>> 6c116d73c17c3f4117c0257d450b859d01b32e90
    


    if i % 10000 == 0:
        print("10k processed")

f = open("Main-Output.txt","w")
f.write(str(vocabulary))
f.close()
#print(vocabulary)