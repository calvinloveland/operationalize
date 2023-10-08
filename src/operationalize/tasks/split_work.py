from operationalize.tasks.task import Task_DAG


split_work_task = Task_DAG(
    dependencies=[],
    dependents=[],
    name="Split Work",
    type="Split Work",
    description="Split work into multiple parts",
    requirements="Split this idea in to two parts",
    workspace="split_text_workspace.html",
    time_limit=60,
    output="Two parts of the idea",
)