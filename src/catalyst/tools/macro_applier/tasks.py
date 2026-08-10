from dataclasses import dataclass, field
from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "assets"


@dataclass(frozen=True)
class Macro:
    name: str
    macro_name: str
    path: Path
    needs_confirmation: bool = False


@dataclass(frozen=True)
class Task:
    name: str
    macros: list[Macro] = field(default_factory=list)


def _macro(
    display_name: str, filename: str, sub_name: str, needs_confirmation: bool = False
) -> Macro:
    return Macro(
        name=display_name,
        macro_name=sub_name,
        path=ASSETS_DIR / filename,
        needs_confirmation=needs_confirmation,
    )


MAIN_TWITTER = _macro("Main Twitter", "Main Twitter.xlsm", "Twitter_Macro_Hesham")
TALKWALKER_TRADITIONAL = _macro(
    "Talkwalker Traditional",
    "Talkwalker Traditional.xlsm",
    "TransformRawToFinal",
    needs_confirmation=True,
)
SOCIAL_FILE_ARRANGEMENT = _macro(
    "Social File Arrangement",
    "Social File Arrangement.xlsm",
    "Run_Tags_MoveDelete_ThenConsolidate",
)
DAILY_REPORT_FORMATTING = _macro(
    "Daily Report Formatting",
    "Daily Report Formatting.xlsm",
    "KeepColumns_ACEFSW_SetWidth_AndHyperlinks",
)

TASKS = [
    Task(name="Standard Workflow", macros=[MAIN_TWITTER, SOCIAL_FILE_ARRANGEMENT]),
    Task(name="Daily Report Excel File", macros=[MAIN_TWITTER, DAILY_REPORT_FORMATTING]),
    Task(name="Traditional Talkwalker", macros=[TALKWALKER_TRADITIONAL]),
    Task(name="Just Social", macros=[MAIN_TWITTER]),
]
