import os
import random

import flask
from flask import request
from loguru import logger

from operationalize.tasks.software_creation import SoftwareCreation
from operationalize.project import NEW_PROJECT

app = flask.Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "tasks/templates"),
    static_url_path="",
)

projects = [NEW_PROJECT]


@app.route("/")
def index():
    request_data = request.args
    project_id = request_data.get("project_id", None)
    worker_id = request_data.get("worker_id", None)
    if worker_id is None:
        worker_id = "HUMAN WORKER " + str(random.randint(0, 1000000))
    return flask.render_template(
        "index.html", project_id=project_id, worker_id=worker_id
    )


@app.route("/next_task/<worker_id>/<project_id>")
def next_task(worker_id, project_id):
    task = projects[project_id].get_next_task(worker_id)
    if task is None:
        return flask.render_template("waiting.html", worker_id=worker_id)
    task.assign(worker_id)
    logger.info(f"Giving task {task.name} to worker {worker_id}")
    return flask.render_template(task.workspace, task=task, worker_id=worker_id)


@app.route("/task/<task_id>", methods=["POST", "GET"])
def submit_task(task_id):
    task = None
    for project in projects.values():
        task = project.get_task_by_id(task_id)
        if task is not None:
            break
    if task is None:
        return "Task not found", 404
    request_data = request.get_json()
    logger.info(f"Completing task {task.name} with data {request_data}")
    task.complete(**request_data)
    return "Task completed"


@logger.catch
def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
