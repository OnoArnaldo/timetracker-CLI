import typing as _
from argparse import Namespace

from . import projects_context, Result, result_ok, ERRORS

if _.TYPE_CHECKING:
    from ..models import Projects, Project


def _list_all(projects: 'Projects') -> Result:
    if not projects.projects:
        print('No projects...')
        return result_ok

    for proj in projects.projects:
        print(f'{proj.str}')

        if not proj.tasks:
            print('    No tasks...')

        for task in proj.tasks:
            print(f'    {task.str}')

    return result_ok


def _list(project: 'Project') -> Result:
    if not project.tasks:
        return Result(ERRORS.FAILED_TO_RUN, f'No tasks for project {project.name!r} [{project.id}].')

    for task in project.tasks:
        print(f'{task.str}')

    return result_ok


def _add(project: 'Project', task_name: str) -> Result:
    if not project.add(task_name):
        return Result(ERRORS.FAILED_TO_RUN, f'[ERROR] unable to add the task {task_name!r} to the project {project.name!r}')
    return result_ok


def _delete(project: 'Project', task_name: str) -> Result:
    if not project.delete(task_name):
        return Result(ERRORS.FAILED_TO_RUN, f'[ERROR] unable to delete the task {task_name!r} from the project {project.name!r}')
    return result_ok


def _edit(project: 'Project', task_name: str) -> Result:
    if task := project.find(task_name):
        while True:
            print(f'Enter the new name for {project.name!r}:{task.name!r}, or "Q" to cancel.')
            new_name = input(f'New name: ')
            if new_name in 'qQ':
                break

            if project.edit(task_name, new_name):
                break
            else:
                print(f'[ERROR] project {new_name!r} already exists.')

        return result_ok

    return Result(ERRORS.FAILED_TO_RUN, f'[ERROR] could not find the task {task_name!r} in the project {project.name!r}')


def run_task(args: Namespace) -> Result:
    with projects_context() as projects:
        if args.project_name == '@' and args.list:
            return _list_all(projects)

        if (project := projects.find(args.project_name)) is None:
            return Result(ERRORS.FAILED_TO_RUN, f'[ERROR] could not find the project {args.project_name!r}')

        if args.list:
            return _list_all(project)

        elif args.add:
            return _add(project, args.add)

        elif args.delete:
            return _delete(project, args.delete)

        elif args.edit:
            return _edit(project, args.edit)

        return Result(ERRORS.INVALID_ARGS)
