import flask
from operationalize.tasks.design_plantuml import DesignPlantUML
import os
app = flask.Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__),'tasks/templates'),static_url_path='')


@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/design_plantuml')
def design_plantuml():
    return DesignPlantUML().route()

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
