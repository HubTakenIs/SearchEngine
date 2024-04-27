import json
from flask import Flask
from flask import request
from flask import render_template
from main import QueryToDocVector, loadDocuments, executeQuery

from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1,x_host=1,x_prefix=1
)
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
    response = ""
    for i in range(5):
        response += f"<div class='panel'><h2>{output[i][2]['title']}</h2>"
        response += f"<div ><p>{output[i][2]['body']}</p> </div></div>"

    return response


 