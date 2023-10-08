import flask
from flask import render_template
from operationalize.tasks.split_work import split_work_task
import os
app = flask.Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__),'tasks/templates'),static_url_path='')


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/split_work')
def split_work():
    return render_template(split_work_task.workspace, task=split_work_task)


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
