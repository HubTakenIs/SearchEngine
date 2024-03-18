import string
import json
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
nltk.download("punkt")
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize


fp = open("reddit_jokes.json","r",1)
jayson = json.load(fp)

# init Sample documents
documents = []

for i in range(0,len(jayson)):
    #retrieve joke
    joke = jayson[i]
    # retrieve text from joke
    title = joke['title']
    body = joke['body']
    documents.append("Title: " +title + " Joke: " + body)
    

# Sample query
query = "russian woman"

# Step 1: Tokenize and preprocess the text
nltk.download('punkt')
from nltk.tokenize import word_tokenize
tokenized_documents = [word_tokenize(doc.lower()) for doc in documents]
tokenized_query = word_tokenize(query.lower())

# Step 2: Calculate TF-IDF
# Convert tokenized documents to text
preprocessed_documents = [' '.join(doc) for doc in tokenized_documents]
preprocessed_query = ' '.join(tokenized_query)

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_documents)

# Transform the query into a TF-IDF vector
query_vector = tfidf_vectorizer.transform([preprocessed_query])

# Step 3: Calculate cosine similarity
cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)

# Step 4: Rank documents by similarity
results = [(documents[i], cosine_similarities[0][i]) for i in range(len(documents))]
results.sort(key=lambda x: x[1], reverse=True)

# Step 5: Print the ranked documents
results = results[:10]

# Print the ranked documents
for doc, similarity in results:
    print(f"Similarity: {similarity:.2f}\n{doc}\n")

'''
nltk.download('punkt')
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

for i in range(0,10001):
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


    if i % 10000 == 0:
        print("10k processed")

f = open("Main-Output.txt","w")
f.write(str(vocabulary))
f.close()
#print(vocabulary)

'''
