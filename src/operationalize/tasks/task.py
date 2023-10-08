class Task_DAG:
    def __init__(self, dependencies, dependents, **kwargs):
        self.dependencies = dependencies
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
        for key in kwargs:
            if key not in expected_kwargs:
                raise ValueError(f"Unexpected keyword argument: {key}")
        for key, value in kwargs.items():
            setattr(self, key, value)
