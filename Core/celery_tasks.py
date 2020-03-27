from celery import Celery
from flask import Flask


def make_celery(app: Flask):
    celery = Celery(
        app.name,
        backend="redis://127.0.0.1:6379",
        broker=app.config['CELERY_RESULT_BACKEND']
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


