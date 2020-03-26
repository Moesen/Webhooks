from flask import Flask, render_template, request, jsonify
import os
import redis
import league_updater

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/send_message", methods=["POST", "GET"])
def send_message():
    if request.method == "POST":
        message = request.form
        username = message["username"]
        content = message["content"]

        league_updater.send_message(username=username,
                                    content=content)

        return render_template("message_sent.html")

if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=5000)
