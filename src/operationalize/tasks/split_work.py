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
        assert kwargs.get("work_chain") is not None
        work_chain = kwargs.get("work_chain")
        if depth == 0:
            self.dependents = [copy.deepcopy(work_chain)]
        else:
            integrate_work = TaskDAG(name="Integrate Work", type="Integrate Work", description="Integrate work from other tasks", time_limit=120, id=self.id + "i")
            split_work_a = SplitWork(depth=depth - 1, id=self.id + "a", work_chain= work_chain)
            split_work_a.append_node(integrate_work)
            split_work_b = SplitWork(depth=depth - 1, id=self.id + "b", work_chain= work_chain)
            split_work_b.append_node(integrate_work)
            self.dependents = [split_work_a, split_work_b]

    def complete(self, **kwargs):
        super().complete(**kwargs)
        # continue_splitting = kwargs.get("continue_splitting", False)
        # TODO: implement more splitting the DAG even further


class IntegrateWork(TaskDAG):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Integrate Work"
        self.type = "Integrate Work"
        self.description = "Integrate work from other tasks"
        self.time_limit = kwargs.get("time_limit", 120)
        self.id = kwargs.get("id", "a")
        self.dependents = [kwargs.get("work_chain")]

    def complete(self, **kwargs):
        super().complete(**kwargs)
        # continue_splitting = kwargs.get("continue_splitting", False)

    def __copy__(self):
        pass

    def __deepcopy__(self):
        pass
