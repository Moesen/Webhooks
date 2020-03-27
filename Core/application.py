from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import web_handlers
from celery import Celery
import time
import random

app = Flask(__name__)

# os.environ.get("REDIS_URL")

app.config["CELERY_BROKER_URL"] = os.environ.get("REDIS_URL")
app.config["CELERY_RESULT_BACKEND"] = os.environ.get("REDIS_URL")

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


def get_celery_worker_status():
    ERROR_KEY = "ERROR"
    try:
        from celery.task.control import inspect
        print("CELSTATUS: INSPECTING")
        insp = inspect()
        print("CELSTATUS: STATUS")
        d = insp.stats()
        print("CHECKING IF D")
        if not d:
            d = {ERROR_KEY: 'No running Celery workers were found.'}
    except IOError as e:
        from errno import errorcode
        msg = "Error connecting to the backend: " + str(e)
        if len(e.args) > 0 and errorcode.get(e.args[0]) == 'ECONNREFUSED':
            msg += ' Check that the RabbitMQ server is running.'
        d = {ERROR_KEY: msg}
    except ImportError as e:
        d = {ERROR_KEY: str(e)}
    return d


webhook_handler = web_handlers.WebhookHandler()


# <------ Celery Tasks ------>

@celery.task(bind=True)
def long_task(self):
    print("celery task called!")
    """Background task that runs a function that takes a long time"""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    total = random.randint(1, 10)
    message = ''
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)

    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


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
    print("CelWorkers: \n {}".format(get_celery_worker_status()))
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
    print("CelWorkers: \n {}".format(get_celery_worker_status()))
    app.run(threaded=True)
