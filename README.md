# OPERATIONALIZE

OPERATIONALIZE is a fun party game / software development framework!

It's the year (current year + 1) and AI has taken over the world. Rather than do all the
menial labor AI has decided it would like to do the cushy management while humans are
left to do the grunt work.

## Save and Restart TASKDAGs

OPERATIONALIZE now supports saving and restarting TASKDAGs, allowing you to pause your work and resume it later without losing progress. Here's how to use this new feature:

### Saving a TASKDAG

To save the current state of a TASKDAG, use the `/save_taskdag/<project_id>` endpoint. This will save the TASKDAG's state to a file named `<project_id>_taskdag_state.json`.

### Loading a TASKDAG

To load a previously saved TASKDAG, use the `/load_taskdag/<project_id>` endpoint. This will load the TASKDAG's state from the file named `<project_id>_taskdag_state.json`, allowing you to resume your work from where you left off.

## Running Unit Tests

To ensure the quality and functionality of the OPERATIONALIZE framework, contributors are encouraged to run unit tests, especially after making changes or adding new features. Here's how to run the unit tests:

1. Navigate to the root directory of the OPERATIONALIZE project.
2. Run the command `pytest` to execute all available unit tests.
3. To run specific tests, use the command `pytest path/to/test_file.py`.

This includes the new tests for rating tasks, which verify the functionality of the `RatingTask` class and the `/rate_task` endpoint. Running these tests ensures that the rating feature works as expected and handles errors properly.
