from operationalize.tasks.task import Task
#import flask render_template
from flask import render_template
import os

class DesignPlantUML(Task):


    def route(self):
        return render_template('design_plantUML_workspace.html')
