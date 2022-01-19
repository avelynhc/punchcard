import os
from flask import Flask

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def get_ping():
    return "pong"

if __name__ == "__main__":
    app.run(port=os.getenv("PORT", 4000), debug=os.getenv("DEBUG", "false") == "true")