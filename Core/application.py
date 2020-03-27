from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import web_handlers
from celery import Celery
import celery_tasks
import time
import random

app = Flask(__name__)

# os.environ.get("REDIS_URL")

app.config["CELERY_BROKER_URL"] = os.environ.get("REDIS_URL")
app.config["CELERY_RESULT_BACKEND"] = os.environ.get("REDIS_URL")

celery = celery_tasks.make_celery(app)
webhook_handler = web_handlers.WebhookHandler()


# <------ Celery Tasks ------>

@celery.task()
def long_task():
    delay = 2
    time.sleep(delay)
    return f"Slept for {delay} seconds"


# <----- MainPage ----->


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/send_message", methods=["POST", "GET"])
def send_message():
    if request.method == "POST":
        message = request.form
        username = message["username"]
        content = message["content"]

        webhook_handler.send_message(username=username,
                                     content=content)

        return redirect(url_for("index"))


@app.route("/send_message_custom_url", methods=["POST", "GET"])
def send_message_custom_url():
    if request.method == "POST":
        message = request.form
        username = message["username"]
        content = message["content"]
        webhook_url = message["webhook_url"]

        webhook_handler.send_message_custom_url(webhook_url,
                                                username=username,
                                                content=content
                                                )

        return redirect(url_for("index"))


# <----- Summoner ----->


@app.route("/summoner_status", methods=["POST", "GET"])
def summoner_status():
    return redirect(url_for("index"))


@app.route("/summoner_edit", methods=["POST", "GET"])
def summoner_edit():
    if request.method == "POST":
        print("post")
    elif request.method == "GET":
        print("get")
    return redirect(url_for("index"))


# <----- Tasks page ----->


@app.route("/tasks", methods=["POST", "GET"])
def tasks():
    return render_template("tasks.html")


@app.route("/tasks/add_long_task", methods=["POST"])
def add_long_task():
    task = long_task.apply_async()
    return jsonify({}), 202, {"Location": url_for("task_status", task_id=task.id)}


@app.route('/status/<task_id>')
def task_status(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


# <------ Misc ------>


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(threaded=True)
