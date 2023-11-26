from operationalize.tasks.task import TaskDAG
import git
import os
from loguru import logger

class TaskSelection(TaskDAG):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.type = "SELECTION"
        self.options = kwargs.get("options",None)
        self.workspace = "selection_workspace.html"



class TaskFromGit(TaskDAG):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.type = "GIT"
        self.url = kwargs.get("url",None)
        self.name = self.url.split("/")[-1].replace(".git","")
        self.task_selection = kwargs.get("task_selection","select")
        if self.task_selection == "select":
            self.append_node(TaskSelection(name="Select a task",description="Select a task from the list below",options=self.tasks))
        elif self.task_selection == "first":
            pass
        elif self.task_selection == "random":
            pass

    def initialize_from_url(self):
        to_path = os.path.join(os.path.join(os.getcwd(),"repos"),self.name)
        repo = git.Repo.clone_from(self.url, to_path)
        todo_path = os.path.join(to_path,"TODO.txt")
        self.tasks = []
        if os.path.exists(todo_path):
            with open(todo_path,"r") as f:
                for line in f.readlines():
                    self.tasks.append(line.strip())
        else:
            logger.error(f"Could not find TODO.txt in {to_path}")
            self.tasks.append("Create TODO.txt in this repo")

            




