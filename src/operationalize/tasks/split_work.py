from operationalize.tasks.task import TaskDAG
import copy


class SplitWork(TaskDAG):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Split Work"
        self.type = "Split Work"
        self.description = "Split work into tasks"
        self.time_limit = kwargs.get("time_limit", 120)
        depth = kwargs.get("depth", 3)
        self.id = kwargs.get("id", "a")
        self.workspace = kwargs.get("workspace", "split_text_workspace.html")
        self.requirements = [
            "Split the work into two complete subtasks.",
            "Tasks should cover all of the work that needs to be done.",
        ]
        assert kwargs.get("work_chain") is not None
        work_chain = kwargs.get("work_chain")
        self.integration_task = kwargs.get("integration_task")
        if depth == 0:
            self.dependents = [copy.deepcopy(work_chain), copy.deepcopy(work_chain)]
        else:
            integrate_work_a = TaskDAG(
                name="Integrate Work",
                type="Integrate Work",
                description="Integrate work from other tasks",
                time_limit=120,
                id=self.id + "ai",
            )
            integrate_work_b = TaskDAG(
                name="Integrate Work",
                type="Integrate Work",
                description="Integrate work from other tasks",
                time_limit=120,
                id=self.id + "bi",
            )
            split_work_a = SplitWork(
                depth=depth - 1,
                id=self.id + "a",
                work_chain=work_chain,
                integration_task=integrate_work_a,
            )
            split_work_a.append_node(integrate_work_a)
            split_work_b = SplitWork(
                depth=depth - 1,
                id=self.id + "b",
                work_chain=work_chain,
                integration_task=integrate_work_b,
            )
            split_work_b.append_node(integrate_work_b)
            self.dependents = [split_work_a, split_work_b]

    def complete(self, **kwargs):
        super().complete(**kwargs)
        assert len(self.dependents) == 2
        assert len(kwargs.get("output")) == 2
        self.dependents[0].requirements.append(
            f"The idea is: {kwargs.get('output')[0]}"
        )
        if isinstance(self.dependents[0], SplitWork):
            self.dependents[0].integration_task.requirements.append(
                "The idea is: " + kwargs.get("output")[0]
            )
        self.dependents[1].requirements.append(
            f"The idea is: {kwargs.get('output')[1]}"
        )
        if isinstance(self.dependents[1], SplitWork):
            self.dependents[1].integration_task.requirements.append(
                "The idea is: " + kwargs.get("output")[1]
            )


class IntegrateWork(TaskDAG):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Integrate Work"
        self.type = "Integrate Work"
        self.description = "Integrate work from other tasks"
        self.time_limit = kwargs.get("time_limit", 120)
        self.id = kwargs.get("id", "a")
        self.dependents = [kwargs.get("work_chain")]
        self.workspace = kwargs.get("workspace", "text_workspace.html")
