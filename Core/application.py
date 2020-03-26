from flask import Flask, render_template, request, redirect, url_for
import os
import league_updater

app = Flask(__name__)
handler = league_updater.WebhookHandler()

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/send_message", methods=["POST", "GET"])
def send_message():
    if request.method == "POST":
        message = request.form
        username = message["username"]
        content = message["content"]

        handler.send_message(username=username,
                             content=content)

        return redirect(url_for("index"))


@app.route("/summoner_status", methods=["POST", "GET"])
def summoner_status():
    return redirect("/")


if __name__ == "__main__":
    app.run(threaded=True)
