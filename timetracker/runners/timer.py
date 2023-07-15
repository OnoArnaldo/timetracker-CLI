import typing as _
from argparse import Namespace

from ..models import Entry, Task
from . import projects_context, Result, result_ok, ERRORS

if _.TYPE_CHECKING:
    from ..models import Projects


def _start(projects: 'Projects', task_name: str) -> Result:
    if projects.current:
        task = projects.current.parent
        proj = task.parent
        return Result(ERRORS.FAILED_TO_RUN, f'[ERROR] the task {proj.name!r}:{task.name!r} is already running.')

    for proj in projects.projects:
        for task in proj.tasks:
            if task.name == task_name or task.id == task_name:
                projects.current = Entry(parent=task)
                print(f'Timer started for task {proj.name!r}:{task.name!r}')
                return result_ok

    return Result(ERRORS.FAILED_TO_RUN, f'Could not find the task {task_name!r}.')


def _status(projects: 'Projects') -> Result:
    if projects.current is None:
        return Result(ERRORS.FAILED_TO_RUN, '[ERROR] no task is running, use "start" command first.')

    entry = projects.current
    entry.set_stop()
    task = entry.parent
    proj = task.parent
    print(f'Project: {proj.str}\n'
          f'Task: {task.str}\n'
          f'Entry: {entry.str}')

    return result_ok


def _pause(projects: 'Projects') -> Result:
    if projects.current is None:
        return Result(ERRORS.FAILED_TO_RUN, f'[ERROR] no task is running, use "start" command first.')

    cur_entry: Entry = projects.current
    cur_task: Task = cur_entry.parent

    cur_entry.set_stop()
    for proj in projects.projects:
        for task in proj.tasks:
            if task.name == cur_task.name:
                task.entries.append(cur_entry)
                projects.current = None
                print(f'Timer paused for task {proj.name!r}:{task.name!r}.')
                return result_ok

    return Result(ERRORS.FAILED_TO_RUN, f'Could not find the task {cur_task.parent.name!r}:{cur_task.name!r}.')


def _cancel(projects: 'Projects') -> Result:
    print(f'Timer canceled for {projects.current.parent.name!r}')
    projects.current = None
    return result_ok


def run_timer(args: Namespace) -> Result:
    with projects_context() as projects:
        if args.start:
            return _start(projects, args.start)

        elif args.status:
            return _status(projects)

        elif args.pause:
            return _pause(projects)

        elif args.cancel:
            return _cancel(projects)

        return Result(ERRORS.INVALID_ARGS)
