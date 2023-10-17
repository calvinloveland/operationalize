from operationalize.tasks.task import TaskDAG
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


class SoftwareCreation(TaskDAG):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Software Creation"
        presentation = TaskDAG(
            name="Presentation",
            type="Presentation",
            description="Present integrated code",
            requirements=["Integrated Code"],
            workspace="presentation.html",
            time_limit=300,
            output="Presentation",
        )
        testing = TaskDAG(
            name="Testing",
            type="Testing",
            description="Test (and fix) the code",
            requirements=["Integrated Code"],
            workspace="testing.html",
            time_limit=180,
            output="Integrated Code",
            dependents=[presentation],
        )
        integration = TaskDAG(
            name="Integration",
            type="Integration",
            description="Integrate code for each task",
            requirements=["Code for each task"],
            workspace="integration.html",
            time_limit=180,
            output="Integrated Code",
            dependents=[testing],
        )
        code = TaskDAG(
            name="Code",
            type="Code",
            description="Create code for each task",
            requirements=["Tests for each task"],
            workspace="code.html",
            time_limit=180,
            output="Code for each task",
            dependents=[integration],
        )
        tests = TaskDAG(
            name="Tests",
            type="Tests",
            description="Create tests for each task",
            requirements=["Tasks"],
            workspace="tests.html",
            time_limit=120,
            output="Tests for each task",
            dependents=[code],
        )

        split_work = TaskDAG(
            name="Split Work",
            type="Split Work",
            description="Split work into tasks",
            requirements=["Brainstorming"],
            workspace="split_work.html",
            time_limit=120,
            output="Tasks",
            depth=3,
            work_chain=tests,
        )
        brainstorming = TaskDAG(
            name="Brainstorming",
            type="Brainstorming",
            description="Brainstorming for something to create",
            requirements=[],
            workspace="brainstorming.html",
            time_limit=120,
            output="Brainstorming",
            dependents=[split_work],
        )
        self.depedencies = [brainstorming]
