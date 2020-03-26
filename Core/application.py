from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return "<h1> Welcome to RehoboamWebhooks"


if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=5000)