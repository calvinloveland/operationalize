import copy

from operationalize.tasks.task import TaskDAG


class SplitWork(TaskDAG):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name", "Split Work")
        depth = kwargs.get("depth", 3)
        self.id = kwargs.get("id", "a")
        self.workspace = kwargs.get("workspace", "split_text_workspace.html")
        self.requirements = [
            "Split the work into two complete subtasks.",
            "Tasks should cover all of the work that needs to be done.",
        ]
        assert kwargs.get("work_chain") is not None
        work_chain = kwargs.get("work_chain")
        if depth == 0:
            self.dependents = [copy.deepcopy(work_chain), copy.deepcopy(work_chain)]
        else:
            split_work_a = SplitWork(
                depth=depth - 1,
                id=self.id + "a",
                work_chain=work_chain,
            )
            split_work_b = SplitWork(
                depth=depth - 1,
                id=self.id + "b",
                work_chain=work_chain,
            )
            self.dependents = [split_work_a, split_work_b]
        integration = TaskDAG(
            name="Integrate Work",
            type="Integrate Work",
            description="Integrate work from other tasks",
            time_limit=120,
            id=self.id + "i",
            completion_text="Integrated work from other tasks:",
        )
        self.append_node(integration)
        self.integration_task = integration

    def complete(self, output):
        super().complete(output)
        assert len(self.dependents) == 2
        assert len(output) == 2
        self.dependents[0].requirements.append(f"The idea is: {output[0]}")
        if isinstance(self.dependents[0], SplitWork):
            self.dependents[0].integration_task.requirements.append(
                "The idea is: " + output[0]
            )
        self.dependents[1].requirements.append(f"The idea is: {output[1]}")
        if isinstance(self.dependents[1], SplitWork):
            self.dependents[1].integration_task.requirements.append(
                "The idea is: " + output[1]
            )
