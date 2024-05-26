import json

def save_task_dag_state(task_dag, file_path):
    """
    Save the state of a TaskDAG to a file.
    """
    with open(file_path, 'w') as file:
        json.dump(task_dag.__dict__, file, default=lambda o: o.__dict__, indent=4)

def load_task_dag_state(task_dag, file_path):
    """
    Load the state of a TaskDAG from a file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
        task_dag.__dict__.update(data)
