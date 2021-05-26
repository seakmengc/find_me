from flask import Flask

import os
from neomodel import db
from commands.crawl import bp as crawl_bp
from commands.stem import bp as stem_bp

app = Flask(__name__)

app.register_blueprint(crawl_bp)
app.register_blueprint(stem_bp)

db.set_connection('bolt://{username}:{password}@{uri}'.format(username=os.getenv('DB_USERNAME'),
                                                              password=os.getenv('DB_PASSWORD'),
                                                              uri=os.getenv('DB_URI')))

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)

