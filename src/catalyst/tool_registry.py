from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Tool:
    name: str
    open: Callable[[], None]


def build_registry(daily_report_open: Callable[[], None]) -> list[Tool]:
    return [Tool(name="Daily Report Generator", open=daily_report_open)]
