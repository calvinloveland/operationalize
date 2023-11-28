from operationalize.tasks.task_selection import SelectionTask


class NextTaskSelection(SelectionTask):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Select a task"
        self.description = "Select a task from the list below"
        self.options = kwargs.get("options", None)
        self.workspace = "selection_workspace.html"
