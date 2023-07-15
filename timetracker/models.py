import hashlib
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Entry:
    parent: 'Task'
    start: datetime = field(default_factory=datetime.utcnow)
    stop: datetime = field(default_factory=datetime.utcnow)

    @property
    def total(self) -> int:
        return int((self.stop - self.start).total_seconds())

    @property
    def total_str(self) -> str:
        minutes, seconds = divmod(self.total, 60)
        hours, minutes = divmod(minutes, 60)
        return f'{hours}h {minutes}min {seconds}s'

    @property
    def str(self) -> str:
        return f'{self.start:%Y-%m-%d %H-%M-%S} -> {self.stop:%Y-%m-%d %H-%M-%S} [{self.total_str}]'

    def set_stop(self) -> None:
        self.stop = datetime.utcnow()


@dataclass
class Task:
    name: str
    parent: 'Project'
    entries: list[Entry] = field(default_factory=list)

    @property
    def id(self):
        return hashlib.shake_128(f'{self.parent.name}#{self.name}'.encode()).hexdigest(2)

    @property
    def total(self) -> int:
        return sum(e.total for e in self.entries)

    @property
    def total_str(self) -> str:
        minutes, seconds = divmod(self.total, 60)
        hours, minutes = divmod(minutes, 60)
        return f'{hours}h {minutes}min {seconds}s'

    @property
    def start(self):
        return min(e.start for e in self.entries) if self.entries else datetime.min

    @property
    def stop(self):
        return max(e.stop for e in self.entries) if self.entries else datetime.min

    @property
    def str(self):
        return (f'[{self.id}] {self.name}: '
                f'{self.start:%Y-%m-%d %H:%M:%S} -> {self.stop:%Y-%m-%d %H:%M:%S} '
                f'[{self.total_str}]')


@dataclass
class Project:
    name: str
    tasks: list[Task] = field(default_factory=list)

    @property
    def id(self):
        return hashlib.shake_128(self.name.encode()).hexdigest(2)

    @property
    def total(self) -> int:
        return sum(t.total for t in self.tasks)

    @property
    def total_str(self) -> str:
        minutes, seconds = divmod(self.total, 60)
        hours, minutes = divmod(minutes, 60)
        return f'{hours}h {minutes}min {seconds}s'

    @property
    def start(self):
        return min(e.start for e in self.tasks) if self.tasks else datetime.min

    @property
    def stop(self):
        return max(e.stop for e in self.tasks) if self.tasks else datetime.min

    @property
    def str(self):
        return (f'[{self.id}] {self.name}: '
                f'{self.start:%Y-%m-%d %H:%M:%S} -> {self.stop:%Y-%m-%d %H:%M:%S} '
                f'[{self.total_str}]')

    def index(self, name: str) -> int:
        for idx, task in enumerate(self.tasks):
            if task.name == name or task.id == name:
                return idx
        return -1

    def exists(self, name: str) -> bool:
        return self.index(name) != -1

    def find(self, name: str) -> Task | None:
        if (idx := self.index(name)) != -1:
            return self.tasks[idx]
        return None

    def add(self, name: str) -> bool:
        if not self.exists(name):
            self.tasks.append(Task(name=name, parent=self))
            return True
        return False

    def delete(self, name: str) -> bool:
        if (idx := self.index(name)) != -1:
            self.tasks.pop(idx)
            return True
        return False

    def edit(self, old_name: str, new_name: str) -> bool:
        if task := self.find(old_name):
            task.name = new_name
            return True
        return False


@dataclass
class Projects:
    projects: list[Project] = field(default_factory=list)
    current: Entry = None

    @property
    def total(self):
        return 0

    def index(self, name: str) -> int:
        for i, proj in enumerate(self.projects):
            if proj.name == name or proj.id == name:
                return i
        return -1

    def exists(self, name: str) -> bool:
        return self.index(name) != -1

    def find(self, name: str) -> Project | None:
        if (idx := self.index(name)) != -1:
            return self.projects[idx]
        return None

    def add(self, name: str) -> bool:
        if self.index(name) == -1:
            self.projects.append(Project(name=name))
            return True
        return False

    def delete(self, name: str) -> bool:
        if (idx := self.index(name)) != -1:
            self.projects.pop(idx)
            return True
        return False

    def edit(self, old_name: str, new_name: str) -> bool:
        if (idx := self.index(old_name)) != -1:
            self.projects[idx].name = new_name
            return True
        return False
