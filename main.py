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
import numpy as np

######## Solution 3 ########
## 1: Importing the necessary data
print("Loading data...")
fp = open("reddit_jokes.json","r",1)
jayson = json.load(fp)
## 2: Text Preprocessing
def preprocess(document):
    # Convert text to lowercase
    document = str(document).lower()
    # Remove punctuation
    document = document.translate(str.maketrans('', '', string.punctuation))
    return document.split()
processedDocuments = [preprocess(joke) for joke in jayson]
print("Data loaded and preprocessed.")
# 3: Create the vocabulary
vocabulary = set()
for doc in processedDocuments:
    vocabulary.update(doc)
vocabulary = list(vocabulary)
print(f"Vocabulary Created with size: {len(vocabulary)}")
# 4: Create the Term Document Matrix
def create_term_doc_matrix(docs, vocab):
    term_doc_matrix = np.zeros((len(vocab), len(docs)))
    for i, word in enumerate(vocab):
        for j, doc in enumerate(docs):
            term_doc_matrix[i, j] = doc.count(word)
    return term_doc_matrix

print("Creating Term Document Matrix...")
term_doc_matrix = create_term_doc_matrix(processedDocuments, vocabulary)
print(term_doc_matrix)
print(f"Term Document Matrix Created with size: {term_doc_matrix.shape}")
# 5: Compute Similarity
def cosine_similarity_matrix(matrix):
    similarity_matrix = np.zeros((matrix.shape[1], matrix.shape[1]))
    for i in range(matrix.shape[1]):
        for j in range(matrix.shape[1]):
           similarity_matrix[i, j] = cosine_similarity(matrix[:, i], matrix[:, j])
    return similarity_matrix

similarity_matrix = cosine_similarity_matrix(term_doc_matrix)
# 6: Retrieve Similar Jokes
def query_vsm(query, docs, vocab, term_doc_matrix):
    query_processed = preprocess(query)
    query_vec = np.zeros(len(vocab))
    for word in query_processed:
        if word in vocab:
            query_vec[vocab.index(word)] += 1
    similarities = [cosine_similarity(query_vec, term_doc_matrix[:, i]) for i in range(term_doc_matrix.shape[1])]
    most_similar_doc_index = np.argmax(similarities)
    return docs[most_similar_doc_index]

query = "woman"
most_similar_document = query_vsm(query, processedDocuments, vocabulary, term_doc_matrix)

print(most_similar_document)




#######################

# nltk.download('punkt')
# nltk.download('stopwords')
# ps = PorterStemmer()
# fp = open("reddit_jokes.json","r",1)

# jayson = json.load(fp)

# print(len(jayson)) # 194553 reddit jokes
# #print(jayson[2]) # first not racist joke
# #mytest = jayson[2]
# #print(type(mytest))

# # vocabulary
# vocabulary = {}

# punctuationList = string.punctuation

# def removePunctuation(text):
#     for punct in punctuationList:
#         #print(f"trying to replace {punct}")
#         text = text.replace(punct,"")
#     text = text.replace("\n"," ")
#     text = text.replace('“',' ')
#     text = text.replace('”',' ')
#     text = text.replace('’',' ')
#     text = text.replace('‘',' ')


#     return text

# stop_words = set(stopwords.words('english'))

# def textToIndex(text):
#     splitText = word_tokenize(text)
#     count = 0
#     jokeIndex = {}
#     for word in splitText:
#         if word.lower() in stop_words:
#             #print("stopword found")
#             count +=1
#             continue
#         else:
#             stemmed = ps.stem(word)
#             if stemmed in jokeIndex.keys():
#                 jokeIndex[stemmed].append(count)
#             else:
#                 jokeIndex[stemmed] = [count]
#                 #print(f"I:{count}  original: {word}    stemmed: {ps.stem(word)}")
#                 count += 1
#     return jokeIndex


# def addIndexToVocabulary(index, jid):
#     for term in index:
#         if term in vocabulary.keys():
#             vocabulary[term][jid] = index[term]
#         else:
#             vocabulary[term] = {jid:index[term]}



# for i in range(0,100):
#     #retrieve joke
#     joke = jayson[i]
#     jid = joke['id']
#     # retrieve text from joke
#     title = joke['title']
#     body = joke['body']
#     # remove punctuation
#     title = removePunctuation(title)
#     body = removePunctuation(body)
    
#     #create each index
#     title_index = textToIndex(title)
#     body_index = textToIndex(body)

#     #addIndexToVocabulary
#     addIndexToVocabulary(title_index,jid)
#     addIndexToVocabulary(body_index,jid)


#     if i % 10000 == 0:
#         print("10k processed")

# f = open("Main-Output.txt","w")
# f.write(str(vocabulary))
# f.close()
#print(vocabulary)


#######################

# fp = open("reddit_jokes.json","r",1)
# jayson = json.load(fp)

# # init Sample documents
# documents = []

# for i in range(0,len(jayson)):
#     #retrieve joke
#     joke = jayson[i]
#     # retrieve text from joke
#     title = joke['title']
#     body = joke['body']
#     documents.append(str(joke))   
    

# # Sample query
# query = "woman"

# # Step 1: Tokenize and preprocess the text
# nltk.download('punkt')
# from nltk.tokenize import word_tokenize
# tokenized_documents = [word_tokenize(doc.lower()) for doc in documents]
# tokenized_query = word_tokenize(query.lower())

# # Step 2: Calculate TF-IDF
# # Convert tokenized documents to text
# preprocessed_documents = [' '.join(doc) for doc in tokenized_documents]
# preprocessed_query = ' '.join(tokenized_query)

# # Create a TF-IDF vectorizer
# tfidf_vectorizer = TfidfVectorizer()
# tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_documents)
# f = open("Main-VectorizerMatrtixOutput.txt","w")
# f.write(str(tfidf_matrix))
# f.close()
# f = open("Main-Vectorizer.txt","w")
# f.write(str(tfidf_vectorizer))
# f.close()

# # Transform the query into a TF-IDF vector
# query_vector = tfidf_vectorizer.transform([preprocessed_query])

# # Step 3: Calculate cosine similarity
# cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)

# # Step 4: Rank documents by similarity
# results = [(documents[i], cosine_similarities[0][i]) for i in range(len(documents))]
# results.sort(key=lambda x: x[1], reverse=True)

# # Step 5: Print the ranked documents
# results = results[:20]

# # Print the ranked documents
# for doc, similarity in results:
#     print(f"Similarity: {similarity:.2f}\n{doc}\n")


