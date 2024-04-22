import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Sample documents
documents = [
]

fp = open("api-backend/source_repository/reddit_jokes.json","r",1)
loadedJson = json.load(fp)

for joke in loadedJson:
    documents.append(joke["title"] + " " + joke["body"])


# Sample query
query = "Pizza in germany"

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
print(query_vector)

# Step 3: Calculate cosine similarity
cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)

# Step 4: Rank documents by similarity
results = [(documents[i], cosine_similarities[0][i]) for i in range(len(documents))]
results.sort(key=lambda x: x[1], reverse=True)

results = results[:10]

# Print the ranked documents
for doc, similarity in results:
    print(f"Similarity: {similarity:.2f}\n{doc}\n")