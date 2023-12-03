from operationalize.tasks.task import TaskDAG


class TaskSelection(TaskDAG):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "SELECTION"
        self.options = kwargs.get("options", None)
        self.workspace = "selection_workspace.html"
