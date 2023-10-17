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
        if depth == 0:
            self.dependents = copy.deepcopy([kwargs.get("work_chain")])
        else:
            self.dependents = [
                SplitWork(depth=depth - 1, id=self.id + "a"),
                SplitWork(depth=depth - 1, id=self.id + "b"),
            ]

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
