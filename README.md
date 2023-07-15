# timetracker with CLI

Simple timer tracker with CLI.

> The idea was to experiment with argparser and CLI, no test was created for this project.
 
## Installation:

Just copy the folder and create a virtual environment.

```shell
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

Make sure the file `main.py` is executable.

```shell
chmod +x main.py
```

In case the virtual environment is not in the same folder,
the first line of `main.py` has to be changed.

```python
#!./venv/bin/python
# ^ change this to the actual python path.
import sys
...
```

## Setup the timetracker

Get help.

```shell
./main.py --help
./main.py project --help
./main.py task --help
./main.py timer --help
```

Create project.

```shell
./main.py project --add <project-name>
```

Create task.

```shell
./main.py task --add <task-name> <project-name or project-id>
```

## Run the timetracker

Get all tasks available (`@` will list all the projects).

```shell
./main.py task --list @
```

Start timer.

```shell
./main.py timer --start <task-name or task-id>
```

Check current status.

```shell
./main.py timer --status
```

Pause timer (This will save the timer).

```shell
./main.py timer --pause
```

Cancel timer (this will not save the timer).

```shell
./main.py timer --cancel
```