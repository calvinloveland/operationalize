from operationalize.tasks.task import TaskDAG
from operationalize.tasks.split_work import SplitWork
import copy

"""
Software Creation
-----------------

1. Brainstorming for something to create
2. Split work into tasks
2.1 Continue splitting work until tasks are small enough
3. Create tests for each task
4. Create code for each task
5. Integrate code for each task
6. Test integrated code
7. Present integrated code

1. -> 2.
2. -> 2.1,2.2
2.1 -> 2.1.1,2.1.2
2.2 -> 2.2.1,2.2.2
2.1.1 -> 2.1.1.1, 2.1.1.2
2.1.2 -> 2.1.2.1, 2.1.2.2
2.2.1 -> so on and so forth






"""

code = TaskDAG(
    name="Code",
    type="Code",
    description="Create code for each task",
    requirements=[],
    workspace="code.html",
    time_limit=180,
    output="Code for each task",
    dependents=[],
)
tests = TaskDAG(
    name="Tests",
    type="Tests",
    description="Create tests for each task",
    requirements=[],
    workspace="tests.html",
    time_limit=120,
    output="Tests for each task",
    dependents=[code],
)

split_work = SplitWork(
    name="Split Work",
    type="Split Work",
    description="Split work into tasks",
    requirements=[
        "Split the work into two complete subtasks.",
        "Tasks should cover all of the work that needs to be done.",
    ],
    workspace="split_text_workspace.html",
    time_limit=120,
    output="Tasks",
    depth=3,
    work_chain=tests,
)


class Brainstorming(TaskDAG):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = ("Brainstorming",)
        self.type = ("Brainstorming",)
        self.description = ("Brainstorming for something to create",)
        self.requirements = (
            ["Come up with a great idea for the human workers to create"],
        )
        self.workspace = ("text_workspace.html",)
        self.time_limit = (120,)
        self.output = ("Brainstorming",)
        self.dependents = [split_work]

    def complete(self, **kwargs):
        super().complete(**kwargs)
        for dependent in self.dependents:
            dependent.requirements.append(f"The idea is: {kwargs.get('output')}")


class SoftwareCreation(TaskDAG):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Software Creation"
        self.workspace = "text_workspace.html"

        brainstorming = Brainstorming()

        self.append_node(brainstorming)
        presentation = TaskDAG(
            name="Presentation",
            type="Presentation",
            description="Present integrated code",
            requirements=["Integrate Code"],
            workspace="presentation.html",
            time_limit=300,
            output="Presentation",
        )
        self.append_node(presentation)
        self.completed = True
