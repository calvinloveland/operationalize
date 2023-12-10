from operationalize.tasks.task import TaskDAG


class Project:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "Untitled Project")
        self.task_dag = kwargs.get("task_dag", None)

    @classmethod
    def configuration_options(cls):
        return {
            "name": {"type": "text", "default": "Untitled Project"},
            "competitive": {"type": "boolean", "default": False},
            "allow_rework": {"type": "boolean", "default": True},
        }


NEW_PROJECT = Project(
    name="New Project",
    task_dag=TaskDAG(
        name="New Project",
        description="Create a new project",
        workspace="new_project_workspace.html",
    ),
)
