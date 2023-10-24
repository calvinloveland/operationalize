import flask
from flask import render_template, request
from operationalize.tasks.software_creation import SoftwareCreation
import os
import random

app = flask.Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "tasks/templates"),
    static_url_path="",
)

current_task = SoftwareCreation()


@app.route("/")
def index():
    request_data = request.args
    worker_id = request_data.get("worker_id", None)
    if worker_id is None:
        worker_id = "HUMAN WORKER " + str(random.randint(0, 1000000))
    return flask.render_template("index.html", task=current_task, worker_id=worker_id)


@app.route("/next_task/<worker_id>")
def next_task(worker_id):
    task = current_task.get_next_task(worker_id)
    if task is None:
        return flask.render_template("waiting.html", worker_id=worker_id)
    task.assign(worker_id)
    print(f"Giving task {task.name} to worker {worker_id}")
    return flask.render_template(task.workspace, task=task, worker_id=worker_id)


@app.route("/task/<task_id>", methods=["POST", "GET"])
def submit_task(task_id):
    task = current_task.get_task_by_id(task_id)
    if task is None:
        return "Task not found", 404
    request_data = request.get_json()
    print(request_data)
    task.complete(**request_data)
    return "Task completed"


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
