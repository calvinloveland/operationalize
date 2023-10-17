import copy


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

    def stitch_branches(self, stitching_node):
        """
        Stitch branches of the workflow together.

        Parameters:
        -----------
        stitching_node : Task
            The task to stitch with.

        Returns:
        --------
        None
        """
        assert len(self.dependents) <= 2
        if len(self.dependents) == 2:
            # If there are two dependents, create a shared stitch and stitch the branches together
            shared_stitch = copy.deepcopy(stitching_node)
            self.dependents[0].stitch_branches(shared_stitch)
            self.dependents[1].stitch_branches(shared_stitch)
        elif len(self.dependents) == 0:
            # If there are no dependents, add the stitching node as a dependent
            self.dependents.append(stitching_node)
        else:
            # If there are more than two dependents, stitch each dependent with the stitching node
            for dependent in self.dependents:
                dependent.stitch_branches(stitching_node)

    def append_node(self, node):
        if len(self.dependents) == 0:
            self.dependents.append(node)
        else:
            for dependent in self.dependents:
                dependent.append_node(node)
        self.print_graph()

    def print_graph(self, indent=0):
        print(" " * indent + self.name)
        for dependent in self.dependents:
            dependent.print_graph(indent + 2)
