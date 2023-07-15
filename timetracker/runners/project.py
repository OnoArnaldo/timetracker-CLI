import typing as _
from argparse import Namespace

from . import projects_context, ERRORS, Result, result_ok

if _.TYPE_CHECKING:
    from ..models import Projects


def _list(projects: 'Projects') -> Result:
    if not projects.projects:
        return Result(ERRORS.FAILED_TO_RUN, 'No project has been created!')

    for proj in projects.projects:
        print(f'{proj.id}: {proj.name}: {len(proj.tasks)}: {proj.total}')

    return result_ok


def _add(projects: 'Projects', name: str) -> Result:
    if not projects.add(name):
        return Result(ERRORS.FAILED_TO_RUN, f'[ERROR] unable to add the project {name!r}.')
    return result_ok


def _delete(projects: 'Projects', name: str) -> Result:
    if not projects.delete(name):
        return Result(ERRORS.FAILED_TO_RUN, f'[ERROR] unable to delete the project {name!r}.')
    return result_ok


def _edit(projects: 'Projects', name: str) -> Result:
    if proj := projects.find(name):
        while True:
            print(f'Enter the new name for {proj.name!r}, or "Q" to cancel.')
            new_name = input(f'New name: ')
            if new_name in 'qQ':
                break

            if projects.edit(name, new_name):
                break
            else:
                print(f'[WARNING] project {new_name!r} already exists.')
        return result_ok

    return Result(ERRORS.FAILED_TO_RUN, f'[ERROR] could not find the project {name!r}.')


def run_project(args: Namespace) -> Result:
    with projects_context() as projects:
        if args.list:
            return _list(projects)

        elif args.add:
            return _add(projects, args.add)

        elif args.delete:
            return _delete(projects, args.delete)

        elif args.edit:
            return _edit(projects, args.edit)

        return Result(ERRORS.INVALID_ARGS)
