import string
import os.path
import json
import pickle
import nltk
import math
nltk.download('stopwords')
nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# class Query:

#     def __init__(self, first, second, operator):
#         self.first = first
#         self.second = second
#         self.operator = operator
#         self.set = ()

#     def intersect(self,documents):

#         # updates set
#     def changeFirst(self,first):
#         self.first = first



def removePunctuation(text,punctuationList):
    for punct in punctuationList:
        text = text.replace(punct,"")
    text = text.replace("\n"," ")
    text = text.replace('“',' ')
    text = text.replace('”',' ')
    text = text.replace('’',' ')
    text = text.replace('‘',' ')
    return text


def textToIndex(text,stop_words,stemmer):
    splitText = word_tokenize(text)
    count = 0
    jokeIndex = {}
    for word in splitText:
        if word.lower() in stop_words:
            #print("stopword found")
            count +=1
            continue
        else:
            stemmed = stemmer.stem(word)
            if stemmed in jokeIndex.keys():
                jokeIndex[stemmed].append(count)
            else:
                jokeIndex[stemmed] = [count]
                #print(f"I:{count}  original: {word}    stemmed: {ps.stem(word)}")
                count += 1
    return jokeIndex


def addIndexToInvertedList(index, jid,InvertedList):
    for term in index:
        if term in InvertedList.keys():
            InvertedList[term][jid] = index[term]
        else:
            InvertedList[term] = {jid:index[term]}

# def booleanRetrieval(InvertedList, query, original_documents):


def processBooleanQuery(query):
    # string in format of keyword AND keyword
    sets = []
    words = query.split()
    currentSet = ()
    for word in words:
        return words

def convertJsonToDict():
    # function to change the format json format into a dict
    # key = index, value = original json 
    fp = open("source_repository/reddit_jokes.json","r",1)
    loadedJson = json.load(fp)
    fp.close()
    documents = {}
    for i in range(0,len(loadedJson)):
        documents[i] = loadedJson[i]
    fileobj = open("documents.bin",'wb')
    pickle.dump(documents,fileobj)
    fileobj.close()

def loadDocuments():
    fileobj = open("documents.bin",'rb')
    documents = pickle.load(fileobj) 
    fileobj.close()
    return documents



def storeInvertedLists(InvertedLists):
    fileobj = open("InvertedLists.bin", 'wb')
    pickle.dump(InvertedLists,fileobj)
    fileobj.close()

def loadInvertedLists():
    fileobj = open("InvertedLists.bin", 'rb')
    InvertedLists = pickle.load(fileobj)
    fileobj.close()
    return InvertedLists

def CalculateTF(InvertedList):
    #Inverted List when it's first created
    mostFrequent = float("-inf")
    for key in InvertedList.keys():
        posting = InvertedList[key]
        if len(posting) > mostFrequent:
            mostFrequent = len(posting)
    

    for key in InvertedList.keys():
        posting = InvertedList[key]
        for pkey in posting.keys():
            tfVal = len(posting[pkey]) / mostFrequent
            posting[pkey] = (posting[pkey],tfVal)
        #tf[key] = InvertedList[key]
    #print(InvertedList)
    return InvertedList

def CalculateIDF(InvertedList):
    # InvertedList with TF values updated. 
    jokeCount = len(InvertedList.keys())
    for key in InvertedList.keys():
        #print(key)
        postings = InvertedList[key]
        jokesContainingTerm = len(postings.keys())
        idfVal = math.log(jokeCount / jokesContainingTerm)
        #print(idfVal)
        InvertedList[key] = (InvertedList[key],idfVal)
    #print(idf)
    return InvertedList

def createInvertedList(documents,stop_words,punctuationList,ps,InvertedList):
    for i in range(0,12):
        #retrieve joke
        joke = documents[i]
        jid = i
        #retrieve text from joke
        title = joke['title']
        body = joke['body']
        # remove punctuation
        title = removePunctuation(title,punctuationList)
        body = removePunctuation(body,punctuationList)
        joke_text = title + " " + body
        joke_index = textToIndex(joke_text,stop_words,ps)
        addIndexToInvertedList(joke_index,jid,InvertedList)

def createVectorSpace(InvertedList):
    vectorSpace = {}
    for key in InvertedList.keys():
        idf = InvertedList[key][1]
        postings = InvertedList[key][0]
        for pkey in postings.keys():
            #print(postings[pkey][1])
            if pkey in vectorSpace.keys():
                vectorSpace[pkey][key] = postings[pkey][1] * idf
            else:
                joke = {key:postings[pkey][1] * idf}
                vectorSpace[pkey] = joke 
    return vectorSpace

def main():
    if os.path.isfile("documents.bin"):
        documents = loadDocuments()
    else:
        convertJsonToDict()
        documents = loadDocuments()
    
    stop_words = set(stopwords.words('english'))
    punctuationList = string.punctuation
    ps = PorterStemmer()
    
    # load cached InvertedLists, if it's None then we should remake it.
    InvertedList = {}

    if os.path.isfile("InvertedLists.bin"):
        print("cached file exists")
        InvertedList = loadInvertedLists()
    else:
        print("cached file not found. creating from scratch, wait a while.")
        createInvertedList(documents,stop_words,punctuationList,ps,InvertedList)
        storeInvertedLists(InvertedList)
    # what up 
    InvertedList = CalculateTF(InvertedList)
    InvertedList = CalculateIDF(InvertedList)
    documentVectorSpace = createVectorSpace(InvertedList)
    print(documentVectorSpace)
    #print(InvertedList)
    #print(InvertedList)

if __name__ == "__main__":
    main()