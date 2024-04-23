import json
from flask import Flask
from flask import request
from flask import render_template
from main import QueryToDocVector, loadDocuments, executeQuery


app = Flask(__name__)
documentVectors = loadDocuments("documentVectorSpace.bin")
documents = loadDocuments("documents.bin")


@app.route("/")

def hello_():
    return render_template("hello.html")

@app.route("/joke-search")
def joke_search(query=None):
    query = request.args.get('query')
    queryVector = QueryToDocVector(query)
    output = executeQuery(queryVector,documentVectors,documents)
    #top5 = []
    response = ""
    for i in range(5):
        response += f"<h2>{output[i][2]['title']}</h2>"
        response += f"<div class='panel'> <p>{output[i][2]['body']}</p> </div>"

    return response
    #return json.dumps(top5)


 