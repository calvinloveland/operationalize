import copy
import uuid


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
        self.printed = False
        self.id = uuid.uuid4()
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
        if self.assigned_to is None and not self.completed:
            return [self]
        else:
            tasks = []
            for task in self.dependents:
                if task.get_open_tasks() is not None:
                    tasks.extend(task.get_open_tasks())

    def count_open_tasks(self):
        if self.get_open_tasks() is None:
            return 0
        return len(self.get_open_tasks())

    def assign(self, worker_id):
        self.assigned_to = worker_id

    def get_next_task(self, worker_id=None):
        print(self.name)
        print(self.completed)
        print(self.assigned_to)
        print(worker_id)
        if not self.completed and (
            self.assigned_to is None or self.assigned_to == worker_id
        ):
            return self
        else:
            if not self.completed:
                print("task is not complete!")
                return None
            for task in self.dependents:
                next_task = task.get_next_task(worker_id)
                if next_task is not None:
                    return next_task
        return None

    def append_node(self, node):
        if node == self:
            print("AAAAAAAAAAAAAAAAH")
            print(node.name)
            return
        if len(self.dependents) == 0:
            self.dependents = [node]
        else:
            for dependent in self.dependents:
                print(dependent)
                assert dependent != self
                dependent.append_node(node)

    def print_graph(self, indent=0):
        if self.printed == False:
            print(" " * indent + self.name + "-" + str(self.id))
            self.printed = True
        for dependent in self.dependents:
            assert dependent != self
            dependent.print_graph(indent + 2)
        self.printed = False

    def complete(self, **kwargs):
        self.completed = True

    def get_task_by_id(self, task_id):
        print(self.name)
        print(self.id)
        print(task_id)
        if str(self.id) == str(task_id):
            print("found task")
            return self
        for dependent in self.dependents:
            task = dependent.get_task_by_id(task_id)
            if task is not None:
                return task
        return None
