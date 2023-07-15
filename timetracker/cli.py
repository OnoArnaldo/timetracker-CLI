import typing as _
from argparse import ArgumentParser

Runner = _.Callable


def build_parser(run_project: Runner, run_task: Runner, run_timer: Runner, run_report: Runner) -> ArgumentParser:
    parser = ArgumentParser()
    subparser = parser.add_subparsers(dest='command', title='commands')

    proj_parser = subparser.add_parser('project', help='Project related command')
    proj_group = proj_parser.add_mutually_exclusive_group()
    proj_group.add_argument('--list', '-l', help='List all projects', action='store_true')
    proj_group.add_argument('--add', '-a', metavar='<project name>', help='Add a new project')
    proj_group.add_argument('--delete', '-d', metavar='<project name>', help='Delete a project')
    proj_group.add_argument('--edit', '-e', metavar='<project name>', help='Edit a project')
    proj_parser.set_defaults(func=run_project)

    task_parser = subparser.add_parser('task', help='Task related command')
    task_group = task_parser.add_mutually_exclusive_group()
    task_group.add_argument('--list', '-l', help='List all tasks', action='store_true')
    task_group.add_argument('--add', '-a', metavar='<task name>')
    task_group.add_argument('--delete', '-d', metavar='<task name>')
    task_group.add_argument('--edit', '-e', metavar='<task name>')
    task_parser.add_argument('project_name', metavar='<project name>', help='use @ for all projects')
    task_parser.set_defaults(func=run_task)

    timer_parser = subparser.add_parser('timer', help='Timer related command')
    timer_group = timer_parser.add_mutually_exclusive_group()
    timer_group.add_argument('--start', '-s', metavar='<task id>', help='Start the timetracker')
    timer_group.add_argument('--status', '-t', action='store_true', help='Status of the timetracker')
    timer_group.add_argument('--pause', '-p', action='store_true', help='Pause the timetracker')
    timer_group.add_argument('--cancel', '-c', action='store_true', help='Cancel the timetracker')
    timer_parser.set_defaults(func=run_timer)

    report_parser = subparser.add_parser('report', help='Print report')
    report_group = report_parser.add_mutually_exclusive_group()
    report_group.add_argument('--list', '-l', help='List all reports', action='store_true')
    report_parser.add_argument('report_name', metavar='<report name>', help='Report name')
    report_parser.set_defaults(func=run_report)

    return parser
