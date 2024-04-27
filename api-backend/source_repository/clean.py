import json

with open ("bad-words.txt", "r") as myFile:
    badwords = myFile.read().splitlines()

badwords = badwords[1:]
print(badwords)


fp = open('reddit_jokes.json','r')
documents = json.load(fp)

cleanDocs = []
for doc in documents:
    isClean = True 
    title = doc["title"]
    body = doc["body"]
    currentJoke = title + " " + body
    currentJoke = currentJoke.lower()
    for i in range(0,len(badwords)):
        badWord = badwords[i]
        if(badWord in currentJoke):
            isClean = False
            break
    if isClean:
        cleanDocs.append(doc) 

writeFile = open("cleanedJokes.json", "w")
json.dump(cleanDocs, writeFile)
writeFile.close()
print("Wrote Clean documents to cleanedJokes.json")
print(len(cleanDocs))


#print(badwords)


