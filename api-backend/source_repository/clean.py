import json

with open ("bad-words.txt", "r") as myFile:
    badwords = myFile.read().splitlines()


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
    titleList = title.split()
    bodyList = body.split()
    for word in titleList:
        if word in badwords:
            isClean = False
            break
    for word in bodyList:
        if word in badwords:
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


