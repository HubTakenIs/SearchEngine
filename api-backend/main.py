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

## function to remove punctuation from text
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
            count +=1
            continue
        else:
            stemmed = stemmer.stem(word)
            if stemmed in jokeIndex.keys():
                jokeIndex[stemmed].append(count)
            else:
                jokeIndex[stemmed] = [count]
                count += 1
    return jokeIndex


def addIndexToInvertedList(index, jid,InvertedList):
    for term in index:
        if term in InvertedList.keys():
            InvertedList[term][jid] = index[term]
        else:
            InvertedList[term] = {jid:index[term]}

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
    fp = open("source_repository/cleanedJokes.json","r",1)
    loadedJson = json.load(fp)
    fp.close()
    documents = {}
    for i in range(0,len(loadedJson)):
        documents[i] = loadedJson[i]
    fileobj = open("documents.bin",'wb')
    pickle.dump(documents,fileobj)
    fileobj.close()

def loadDocuments(documentName):
    fileobj = open(documentName,'rb')
    documents = pickle.load(fileobj) 
    fileobj.close()
    return documents



def storeObjectAsBinary(Object,fileName):
    fileobj = open(fileName, 'wb')
    pickle.dump(Object,fileobj)
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
            tfVal = len(posting[pkey])
            #tfVal = len(posting[pkey]) / mostFrequent
            posting[pkey] = (posting[pkey],tfVal)
    return InvertedList

def CalculateIDF(InvertedList):
    # InvertedList with TF values updated. 
    jokeCount = len(InvertedList.keys())
    for key in InvertedList.keys():
        #print(key)
        postings = InvertedList[key]
        jokesContainingTerm = len(postings.keys())
        idfVal = math.log(jokeCount / jokesContainingTerm)
        InvertedList[key] = (InvertedList[key],idfVal)
    return InvertedList

def createInvertedList(documents,stop_words,punctuationList,ps,InvertedList):
    for i in range(0, len(documents)):
        #retrieve joke
        joke = documents[i]
        jid = i
        #retrieve text from joke
        title = joke['title']
        body = joke['body']
        # remove punctuation
        title = removePunctuation(title,punctuationList)
        body = removePunctuation(body,punctuationList)
        # store joke as string
        joke_text = title + " " + body
        # create index for joke
        joke_index = textToIndex(joke_text,stop_words,ps)
        # add index to inverted list
        addIndexToInvertedList(joke_index,jid,InvertedList)

def createVectorSpace(InvertedList):
    vectorSpace = {}
    for key in InvertedList.keys():
        idf = InvertedList[key][1]
        postings = InvertedList[key][0]
        for pkey in postings.keys():
            if pkey in vectorSpace.keys():
                vectorSpace[pkey][key] = postings[pkey][1] * idf
            else:
                joke = {key:postings[pkey][1] * idf}
                vectorSpace[pkey] = joke 
    return vectorSpace


def QueryToDocVector(input):
    vector = {}
    punctuationList = string.punctuation
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    input = removePunctuation(input,punctuationList)
    inputIndex = textToIndex(input,stop_words,ps)
    invertedIndex = {}
    addIndexToInvertedList(inputIndex,-1,invertedIndex)
    invertedIndex = CalculateTF(invertedIndex)
    for key in invertedIndex.keys():
        vector[key] = invertedIndex[key][-1][1]
    ##print(invertedIndex)
    return vector

def RSV(queryVector,documentVector):    
    RSV = 0
    for qterm in queryVector.keys():
        if qterm in documentVector.keys():
            RSV += queryVector[qterm] * documentVector[qterm]
        else:
            RSV += queryVector[qterm] * 0
    return RSV

def executeQuery(query,documentVectors,documents):
    output = []
    for key in list(documentVectors.keys()):
        similarity = RSV(query,documentVectors[key])
        output.append((key,similarity,documents[key]))
    
    output.sort(key=lambda tup: tup[1],reverse=True)
    return output

def main():
    ## If the documents.bin file exists, load it. Otherwise, convert the json and load it.
    if os.path.isfile("documents.bin"):
        documents = loadDocuments("documents.bin")
    else:
        convertJsonToDict()
        documents = loadDocuments("documents.bin")
    
    # define the stop words, punctuation, and stemmer
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
        storeObjectAsBinary(InvertedList, "InvertedLists.bin")
    
    # calculate TF and IDF
    InvertedList = CalculateTF(InvertedList)
    InvertedList = CalculateIDF(InvertedList)
    # if documentVectorSpace exists, load it. Otherwise, create it.
    if os.path.isfile("documentVectorSpace.bin"):
        documentVectorSpace = loadDocuments("documentVectorSpace.bin")
    else:
        documentVectorSpace = createVectorSpace(InvertedList)
        storeObjectAsBinary(documentVectorSpace, "documentVectorSpace.bin")

    vectorQuery = QueryToDocVector("Pizza in germany")
    output = executeQuery(vectorQuery,documentVectorSpace,documents)
    
    for item in output[0:10]:
        print("-----------")
        print(f"key {item[0]}")
        print(f"RSV {item[1]}")
        print(f"Joke {item[2]}")
        print("-----------")
        
        
    


if __name__ == "__main__":
    main()

