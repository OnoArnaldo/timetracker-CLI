#!./venv/bin/python
import sys
from argparse import Namespace
from pathlib import Path

import timetracker.runners.project
import timetracker.runners.task
import timetracker.runners.timer
from timetracker.cli import build_parser
from timetracker import runners as r

root = Path(__file__).parent.absolute()
r.set_pickled(root / 'projects.pickle')


def main() -> int:
    parser = build_parser(timetracker.runners.project.run_project, timetracker.runners.task.run_task,
                          timetracker.runners.timer.run_timer,
                          timetracker.runners.project.run_project)
    args: Namespace = parser.parse_args()

    if args.command in ('project', 'task', 'report', 'timer'):
        result: r.Result = args.func(args)
        if result.error == r.ERRORS.FAILED_TO_RUN:
            print(result.message)
        elif result.error == r.ERRORS.INVALID_ARGS:
            parser.parse_args([args.command, '-h'])

    else:
        parser.print_help()

    return 0


if __name__ == '__main__':
    sys.exit(main())
