import flask
from flask import render_template
from operationalize.tasks.split_work import example_split_work_task
from operationalize.tasks.software_creation import SoftwareCreation
import os

app = flask.Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "tasks/templates"),
    static_url_path="",
)

current_task = SoftwareCreation()


@app.route("/")
def index():
    return flask.render_template("index.html", project=example_split_work_task)


@app.route("/split_work")
def split_work():
    return render_template(
        example_split_work_task.workspace, task=example_split_work_task
    )


@app.route("next_task/<worker_id>")
def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
