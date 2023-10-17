class TaskDAG:
    def __init__(self, dependents=None, **kwargs):
        if dependents is None:
            dependents = []
        self.dependents = dependents
        expected_kwargs = [
            "name",
            "type",
            "description",
            "requirements",
            "workspace",
            "time_limit",
            "output",
        ]
        self.completed = False
        self.assigned_to = None
        for key in kwargs:
            if key not in expected_kwargs:
                raise ValueError(f"Unexpected keyword argument: {key}")
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_expected_completion_time(self):
        if len(self.dependents) == 0:
            return self.time_limit
        dependent_time = max(
            [d.get_expected_completion_time() for d in self.dependents]
        )
        return self.time_limit + dependent_time

    def get_final(self):
        if len(self.dependents) == 0:
            return self
        return self.dependents[0].get_final()

    def get_open_tasks(self):
        for task in self.depedencies:
            if not task.completed:
                return []
        if self.assigned_to is None and not self.completed:
            return [self]
        else:
            tasks = []
            for task in self.dependents:
                tasks.extend(task.get_open_tasks())

    def count_open_tasks(self):
        return len(self.get_open_tasks())

    def assign(self, worker_id):
        self.assigned_to = worker_id

    def complete(self, **kwargs):
        self.completed = True
