from flask import Flask,jsonify, render_template, request
from elasticsearch import Elasticsearch, RequestsHttpConnection
import os
import warnings
warnings.filterwarnings("ignore")
app = Flask(__name__)
DEBUG = os.environ.get("FLASK_DEBUG") == "1"
app.config.update(DEBUG=DEBUG, JSON_PRETTYPRINT_REGULAR=DEBUG)
host = 'https://tux-es1.cci.drexel.edu:9200/ms4976_info624_201904_newsproject/'
es = Elasticsearch(hosts=host,verify_certs=False,http_auth='ms4976:Phooh3ahkei7',connection_class=RequestsHttpConnection,)

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["keywords"]
    # res = es.search(body={"query":{"match" :{"title" :{"query" : search_term}}}})
    # res = es.search(body={"from":0, "size":10, "query": {"multi_match": {"query": search_term, "fields": ["source", "author^2","title", "description"]}}})
    res = es.search(body={"from": 0, "size": 10, "query":{"bool":{"must":[{"multi_match":{"query": str(search_term),"fields": ["source^3", "author^5", "title^2", "description"]}}],"should":{"rank_feature":{"field": "timestamp","sigmoid":{"pivot": 5,"exponent":0.6}}}}} })
    return render_template("results.html", res = res)
    # return jsonify(res['hits']['hits'][:3])
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='localhost', port=8000)
