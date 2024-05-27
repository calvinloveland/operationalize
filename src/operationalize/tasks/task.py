import copy
import uuid
import json
from loguru import logger


class TaskDAG:
    def __init__(self, **kwargs):
        self.dependents = kwargs.get("dependents", [])
        assert self.dependents is not None
        self.dependencies = kwargs.get("dependencies", [])
        self.name = kwargs.get("name", "TASK WITH NO NAME")
        self.type = kwargs.get("type", "TASK WITH NO TYPE")
        self.description = kwargs.get("description", "TASK WITH NO DESCRIPTION")
        self.workspace = kwargs.get("workspace", "text_workspace.html")
        self.time_limit = kwargs.get("time_limit", 120)
        self.requirements = kwargs.get("requirements", [])
        self.id = kwargs.get("id", uuid.uuid4())
        self.completion_text = kwargs.get("completion_text", None)
        self.completed = False
        self.assigned_to = None
        self.printed = False
        self.output = None

    def __deepcopy__(self, memo):
        cls = self.__class__
        new_task = cls.__new__(cls)
        memo[id(self)] = new_task
        for k, v in self.__dict__.items():
            setattr(new_task, k, copy.deepcopy(v, memo))
        new_task.id = uuid.uuid4()
        return new_task

    def to_mermaid_flowchart(self, prepend="flowchart TD\n"):
        chart = prepend
        for dependent in self.dependents:
            chart += (
                str(self.name).replace(" ", "")
                + str(self.id)
                + " --> "
                + str(dependent.name).replace(" ", "")
                + str(dependent.id)
                + "\n"
            )
            chart += dependent.to_mermaid_flowchart(prepend="")
        return chart

    def update_dependencies(self):
        for dependent in self.dependents:
            if self not in dependent.dependencies:
                dependent.dependencies.append(self)
            dependent.update_dependencies()

    def get_expected_completion_time(self):
        if len(self.dependents) == 0:
            return self.time_limit
        dependent_time = max(d.get_expected_completion_time() for d in self.dependents)
        return self.time_limit + dependent_time

    def get_final(self):
        if len(self.dependents) == 0:
            return self
        return self.dependents[0].get_final()

    def get_open_tasks(self):
        if self.task_is_ready():
            return set([self])
        tasks = set()
        for task in self.dependents:
            if task.get_open_tasks() is not None:
                for task in task.get_open_tasks():
                    tasks.add(task)
        return tasks

    def count_open_tasks(self):
        return len(self.get_open_tasks())

    def assign(self, worker_id):
        self.assigned_to = worker_id

    def task_is_ready(self, worker_id=None):
        return (
            not self.completed
            and (self.assigned_to is None or self.assigned_to == worker_id)
            and all(d.completed for d in self.dependencies)
        )

    def get_next_task(self, worker_id=None):
        self.update_dependencies()
        logger.info(f"Getting next task for worker {worker_id}")
        if self.task_is_ready(worker_id):
            return self
        if not self.completed:
            logger.info(f"Task {self.name} is not ready")
            return None
        for task in self.dependents:
            next_task = task.get_next_task(worker_id)
            if next_task is not None:
                return next_task
        return None

    def append_node(self, node):
        if node == self:
            logger.warning(f"Node is already at the end of graph: {node.name}")
            return
        if len(self.dependents) == 0:
            self.dependents = [node]
        else:
            for dependent in self.dependents:
                if dependent is not None:
                    assert dependent != self
                    dependent.append_node(node)

    def print_graph(self, indent=0):
        if not self.printed:
            logger.info(" " * indent + self.name)
            self.printed = True
        for dependent in self.dependents:
            assert dependent != self
            dependent.print_graph(indent + 2)
        self.printed = False

    def complete(self, output):
        def pretty_print(output):
            if isinstance(output, list):
                return "\n".join([str(o) for o in output])
            return str(output)

        self.completed = True
        self.output = output
        if self.completion_text is not None:
            for dependent in self.dependents:
                logger.info(f"Adding completion text to {dependent.name}")
                dependent.requirements.append(
                    self.completion_text + " " + pretty_print(output)
                )
        else:
            logger.warning(f"No completion text for {self.name}")

    def get_task_by_id(self, task_id):
        logger.info(f"Looking for task {task_id} in {self.name}")
        if str(self.id) == str(task_id):
            logger.info(f"Found task {self.name}")
            return self
        for dependent in self.dependents:
            task = dependent.get_task_by_id(task_id)
            if task is not None:
                return task
        return None

    def save_state(self, file_path):
        """Save the current state of the TaskDAG to a file."""
        with open(file_path, "w") as file:
            json.dump(self.__dict__, file, default=default_serializer, indent=4)

    def load_state(self, file_path):
        """Load the TaskDAG state from a file."""
        with open(file_path, "r") as file:
            data = json.load(file)
            self.__dict__.update(data)


def default_serializer(o):
    if isinstance(o, uuid.UUID):
        return str(o)
    return o.__dict__
