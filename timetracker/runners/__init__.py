import typing as _
import pickle
from contextlib import contextmanager
from dataclasses import dataclass

if _.TYPE_CHECKING:
    from pathlib import Path
    from ..models import Projects

_pickled: 'Path | None' = None


def set_pickled(pickled: 'Path') -> None:
    global _pickled
    _pickled = pickled


def load_projects() -> 'Projects':
    if _pickled.exists():
        with _pickled.open('rb') as f:
            return pickle.load(f)
    return Projects()


def dump_projects(projects: 'Projects') -> None:
    with _pickled.open('wb') as f:
        pickle.dump(projects, f, pickle.HIGHEST_PROTOCOL)


@contextmanager
def projects_context() -> _.Generator['Projects', _.Any, None]:
    projects = load_projects()
    try:
        yield projects
    finally:
        dump_projects(projects)


class ERRORS:
    NONE = ''
    INVALID_ARGS = 'invalid_args'
    FAILED_TO_RUN = 'failed_to_run'


@dataclass
class Result:
    error: str = ERRORS.NONE
    message: str = ''


result_ok = Result()
