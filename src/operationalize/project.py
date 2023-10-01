from operationalize.tasks.task import Task
from operationalize.tasks.split_work import SplitWork
from operationalize.tasks.design import Design
from operationalize.tasks.develop import Develop
from operationalize.tasks.integrate import Integrate
from operationalize.tasks.test import Test
from operationalize.tasks.quality_assure import QualityAssure


from flask import render_template


def Project(Task):

    def __init__(self, name, requirements, deliverable_description, tasks):
        super().__init__(name, requirements, deliverable_description)
        self.tasks = tasks



def display_project_creation_form():
    split_work_1 = SplitWork("Split Work", "A list of tasks", "A list of tasks", 60)
    split_work_2 = SplitWork("Split Work", "A list of tasks", "A list of tasks", 60)
    design = Design("Design", "A list of tasks", "A list of tasks", 180)
    develop = Develop("Develop", "A list of tasks", "A list of tasks", 180)
    integrate = Integrate("Integrate", "A list of tasks", "A list of tasks", 60)
    test = Test("Test", "A list of tasks", "A list of tasks", 60)
    quality_assure = QualityAssure("Quality Assure", "A list of tasks", "A list of tasks", 60)


    example_project = Project("Example Project","Do cool stuff!", "A cool thing",[split_work_1, split_work_2, design, develop, integrate, test, quality_assure])
    return render_template('project_creation_form.html', project=example_project)
