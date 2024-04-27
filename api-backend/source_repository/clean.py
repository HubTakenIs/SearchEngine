import json

with open ("bad-words.txt", "r") as myFile:
    badwords = myFile.read().splitlines()

badwords = badwords[1:]
print(badwords)

def convertJsonToDict():
    fp = open("reddit_jokes.json","r",1)
    loadedJson = json.load(fp)
    fp.close()
    documents = {}
    for i in range(0,len(loadedJson)):
        documents[i] = loadedJson[i]
    return documents

documents = convertJsonToDict()

cleanDocs = {}
for doc in documents:
    isClean = True 
    currentDoc = documents[doc]
    title = currentDoc["title"]
    body = currentDoc["body"]
    currentJoke = title + " " + body
    currentJoke = currentJoke.lower()
    for i in range(0,len(badwords)):
        badWord = badwords[i]
        if(badWord in currentJoke):
            isClean = False
            break
    if isClean:
        cleanDocs[doc] = currentDoc

writeFile = open("cleanedJokes.json", "w")
json.dump(cleanDocs, writeFile)
writeFile.close()
print("Wrote Clean documents to cleanedJokes.json")
print(len(cleanDocs))


#print(badwords)


