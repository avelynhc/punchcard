import os

from flask import Flask

app = Flask(__name__)

@app.route('/ping', methods=["GET"])
def ping_pong():
    return 'pong'

if __name__ == '__main__':
    app.run(
        debug=os.environ.get("DEBUG", default="false") == "true",
        host="0.0.0.0",
        port=os.environ.get('PORT', default=5000),
    )
