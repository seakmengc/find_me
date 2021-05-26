from abc import ABC
from urllib import robotparser

import requests
import xmltodict
from flask import Flask
from neo4j import GraphDatabase
import os, json
from neomodel import db, StructuredNode, StringProperty, RelationshipTo
from commands.crawl import bp as crawl_bp

app = Flask(__name__)

app.register_blueprint(crawl_bp)

db.set_connection('bolt://{username}:{password}@{uri}'.format(username=os.getenv('DB_USERNAME'),
                                                              password=os.getenv('DB_PASSWORD'),
                                                              uri=os.getenv('DB_URI')))

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)

