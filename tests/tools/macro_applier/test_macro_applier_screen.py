from pathlib import Path
from unittest.mock import MagicMock

import customtkinter as ctk
import pytest

from catalyst.tools.macro_applier.screen import MacroApplierScreen


@pytest.fixture(scope="module")
def root():
    instance = ctk.CTk()
    yield instance
    instance.destroy()


def test_selecting_a_file_displays_its_name(root, tmp_path, monkeypatch):
    target_path = tmp_path / "target.xlsx"
    target_path.touch()

    screen = MacroApplierScreen(root, on_back=lambda: None)
    monkeypatch.setattr(
        "catalyst.tools.macro_applier.screen.filedialog.askopenfilename",
        lambda **kwargs: str(target_path),
    )

    screen.select_target_file()

    assert screen.target_path == target_path
    assert screen.file_label.cget("text") == target_path.name


def test_the_file_picker_accepts_both_xlsx_and_xlsm(root, monkeypatch):
    screen = MacroApplierScreen(root, on_back=lambda: None)
    seen_kwargs = {}
    monkeypatch.setattr(
        "catalyst.tools.macro_applier.screen.filedialog.askopenfilename",
        lambda **kwargs: seen_kwargs.update(kwargs) or "",
    )

    screen.select_target_file()

    label, pattern = seen_kwargs["filetypes"][0]
    assert "*.xlsx" in pattern
    assert "*.xlsm" in pattern


def test_task_dropdown_lists_all_four_tasks_and_defaults_to_the_first(root):
    screen = MacroApplierScreen(root, on_back=lambda: None)

    assert screen.task_dropdown.cget("values") == [
        "Standard Workflow",
        "Daily Report Excel File",
        "Traditional Talkwalker",
        "Just Social",
    ]
    assert screen.task_dropdown.get() == "Standard Workflow"


@pytest.mark.parametrize(
    "task_name,macro_name",
    [("Just Social", "Main Twitter"), ("Traditional Talkwalker", "Talkwalker Traditional")],
)
def test_selecting_a_single_macro_task_renders_exactly_one_numbered_button(
    root, task_name, macro_name
):
    screen = MacroApplierScreen(root, on_back=lambda: None)

    screen.task_dropdown.set(task_name)
    screen._on_task_selected(task_name)

    buttons = screen.macro_buttons
    assert len(buttons) == 1
    assert buttons[0].cget("text") == f"1. {macro_name}"


@pytest.mark.parametrize(
    "task_name,macro_names",
    [
        ("Standard Workflow", ["Main Twitter", "Social File Arrangement"]),
        ("Daily Report Excel File", ["Main Twitter", "Daily Report Formatting"]),
    ],
)
def test_selecting_a_multi_macro_task_renders_correctly_numbered_and_labeled_buttons(
    root, task_name, macro_names
):
    screen = MacroApplierScreen(root, on_back=lambda: None)

    screen.task_dropdown.set(task_name)
    screen._on_task_selected(task_name)

    buttons = screen.macro_buttons
    assert [b.cget("text") for b in buttons] == [
        f"{i}. {name}" for i, name in enumerate(macro_names, start=1)
    ]


def test_switching_tasks_rebuilds_the_button_row(root):
    screen = MacroApplierScreen(root, on_back=lambda: None)

    screen.task_dropdown.set("Standard Workflow")
    screen._on_task_selected("Standard Workflow")
    assert [b.cget("text") for b in screen.macro_buttons] == [
        "1. Main Twitter",
        "2. Social File Arrangement",
    ]

    screen.task_dropdown.set("Just Social")
    screen._on_task_selected("Just Social")
    assert [b.cget("text") for b in screen.macro_buttons] == ["1. Main Twitter"]
    assert screen.macro_button_row.winfo_children() == screen.macro_buttons


def test_clicking_a_macro_button_applies_it_and_shows_a_success_message(root, tmp_path, monkeypatch):
    target_path = tmp_path / "target.xlsx"
    target_path.touch()

    screen = MacroApplierScreen(root, on_back=lambda: None)
    screen.target_path = target_path
    screen.task_dropdown.set("Just Social")
    screen._on_task_selected("Just Social")

    session = MagicMock()
    session.target_path = target_path.resolve()
    session.apply.return_value = ("DONE", "Done.")
    session_cls = MagicMock(return_value=session)
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.MacroSession", session_cls)
    shown = MagicMock()
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.showinfo", shown)

    screen.macro_buttons[0].cget("command")()

    from catalyst.tools.macro_applier.tasks import MAIN_TWITTER

    session_cls.assert_called_once_with(target_path.resolve())
    session.apply.assert_called_once_with(MAIN_TWITTER.path, MAIN_TWITTER.macro_name)
    shown.assert_called_once()
    assert "Done." in shown.call_args.args[1]


def test_a_second_macro_on_the_same_file_reuses_the_open_session(root, tmp_path, monkeypatch):
    target_path = tmp_path / "target.xlsx"
    target_path.touch()

    screen = MacroApplierScreen(root, on_back=lambda: None)
    screen.target_path = target_path
    screen.task_dropdown.set("Standard Workflow")
    screen._on_task_selected("Standard Workflow")

    session = MagicMock()
    session.target_path = target_path.resolve()
    session.apply.return_value = ("DONE", "Done.")
    session_cls = MagicMock(return_value=session)
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.MacroSession", session_cls)
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.showinfo", MagicMock())

    screen.macro_buttons[0].cget("command")()
    screen.macro_buttons[1].cget("command")()

    session_cls.assert_called_once_with(target_path.resolve())
    assert session.apply.call_count == 2


def test_a_macro_on_a_different_file_opens_a_new_session(root, tmp_path, monkeypatch):
    first_path = tmp_path / "first.xlsx"
    first_path.touch()
    second_path = tmp_path / "second.xlsx"
    second_path.touch()

    screen = MacroApplierScreen(root, on_back=lambda: None)
    screen.task_dropdown.set("Just Social")
    screen._on_task_selected("Just Social")

    sessions = [
        MagicMock(target_path=first_path.resolve(), apply=MagicMock(return_value=("DONE", "Done."))),
        MagicMock(target_path=second_path.resolve(), apply=MagicMock(return_value=("DONE", "Done."))),
    ]
    session_cls = MagicMock(side_effect=sessions)
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.MacroSession", session_cls)
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.showinfo", MagicMock())

    screen.target_path = first_path
    screen.macro_buttons[0].cget("command")()
    screen.target_path = second_path
    screen.macro_buttons[0].cget("command")()

    assert session_cls.call_count == 2


def test_returning_to_a_previously_selected_file_reuses_its_still_open_session(
    root, tmp_path, monkeypatch
):
    first_path = tmp_path / "first.xlsx"
    first_path.touch()
    second_path = tmp_path / "second.xlsx"
    second_path.touch()

    screen = MacroApplierScreen(root, on_back=lambda: None)
    screen.task_dropdown.set("Just Social")
    screen._on_task_selected("Just Social")

    session1 = MagicMock(target_path=first_path.resolve(), apply=MagicMock(return_value=("DONE", "Done.")))
    session2 = MagicMock(target_path=second_path.resolve(), apply=MagicMock(return_value=("DONE", "Done.")))
    session_cls = MagicMock(side_effect=[session1, session2])
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.MacroSession", session_cls)
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.showinfo", MagicMock())

    screen.target_path = first_path
    screen.macro_buttons[0].cget("command")()  # constructs session1
    screen.target_path = second_path
    screen.macro_buttons[0].cget("command")()  # constructs session2
    screen.target_path = first_path
    screen.macro_buttons[0].cget("command")()  # must reuse session1, not construct a 3rd

    assert session_cls.call_count == 2
    assert session1.apply.call_count == 2
    assert session2.apply.call_count == 1


def test_a_failed_apply_shows_a_friendly_message_and_clears_the_session(root, tmp_path, monkeypatch):
    target_path = tmp_path / "target.xlsx"
    target_path.touch()

    screen = MacroApplierScreen(root, on_back=lambda: None)
    screen.target_path = target_path
    screen.task_dropdown.set("Just Social")
    screen._on_task_selected("Just Social")

    session = MagicMock()
    session.target_path = target_path.resolve()
    session.apply.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "catalyst.tools.macro_applier.screen.MacroSession", MagicMock(return_value=session)
    )
    shown_error = MagicMock()
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.showerror", shown_error)

    screen.macro_buttons[0].cget("command")()

    shown_error.assert_called_once_with("Catalyst", "Couldn't apply Main Twitter:\nboom")
    assert target_path.resolve() not in screen.sessions


def test_clicking_a_macro_with_no_target_file_selected_shows_a_guard_message(
    root, monkeypatch
):
    screen = MacroApplierScreen(root, on_back=lambda: None)
    screen.task_dropdown.set("Just Social")
    screen._on_task_selected("Just Social")

    session_cls = MagicMock()
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.MacroSession", session_cls)
    shown_error = MagicMock()
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.showerror", shown_error)

    screen.macro_buttons[0].cget("command")()

    shown_error.assert_called_once_with("Catalyst", "Please select an Excel file first.")
    session_cls.assert_not_called()


def test_a_confirmation_macro_asks_before_applying_and_shows_the_final_message(
    root, tmp_path, monkeypatch
):
    target_path = tmp_path / "target.xlsx"
    target_path.touch()

    screen = MacroApplierScreen(root, on_back=lambda: None)
    screen.target_path = target_path
    screen.task_dropdown.set("Traditional Talkwalker")
    screen._on_task_selected("Traditional Talkwalker")

    session = MagicMock()
    session.target_path = target_path.resolve()
    session.apply.side_effect = [
        ("CONFIRM", "Rows to convert: 5. Continue?"),
        ("DONE", "5 rows converted successfully."),
    ]
    monkeypatch.setattr(
        "catalyst.tools.macro_applier.screen.MacroSession", MagicMock(return_value=session)
    )
    asked = MagicMock(return_value=True)
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.askyesno", asked)
    shown = MagicMock()
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.showinfo", shown)

    from catalyst.tools.macro_applier.tasks import TALKWALKER_TRADITIONAL

    screen.macro_buttons[0].cget("command")()

    asked.assert_called_once_with("Catalyst", "Rows to convert: 5. Continue?")
    assert session.apply.call_args_list == [
        ((TALKWALKER_TRADITIONAL.path, TALKWALKER_TRADITIONAL.macro_name, False),),
        ((TALKWALKER_TRADITIONAL.path, TALKWALKER_TRADITIONAL.macro_name, True),),
    ]
    shown.assert_called_once()
    assert "5 rows converted successfully." in shown.call_args.args[1]


def test_declining_the_confirmation_stops_before_applying_anything(root, tmp_path, monkeypatch):
    target_path = tmp_path / "target.xlsx"
    target_path.touch()

    screen = MacroApplierScreen(root, on_back=lambda: None)
    screen.target_path = target_path
    screen.task_dropdown.set("Traditional Talkwalker")
    screen._on_task_selected("Traditional Talkwalker")

    session = MagicMock()
    session.target_path = target_path.resolve()
    session.apply.return_value = ("CONFIRM", "Continue?")
    monkeypatch.setattr(
        "catalyst.tools.macro_applier.screen.MacroSession", MagicMock(return_value=session)
    )
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.askyesno", MagicMock(return_value=False))
    shown = MagicMock()
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.showinfo", shown)

    screen.macro_buttons[0].cget("command")()

    session.apply.assert_called_once()
    shown.assert_not_called()


def test_an_error_status_shows_as_an_error_dialog_not_an_info_dialog(root, tmp_path, monkeypatch):
    target_path = tmp_path / "target.xlsx"
    target_path.touch()

    screen = MacroApplierScreen(root, on_back=lambda: None)
    screen.target_path = target_path
    screen.task_dropdown.set("Just Social")
    screen._on_task_selected("Just Social")

    session = MagicMock()
    session.target_path = target_path.resolve()
    session.apply.return_value = ("ERROR", "Missing sheet 'Tags'.")
    monkeypatch.setattr(
        "catalyst.tools.macro_applier.screen.MacroSession", MagicMock(return_value=session)
    )
    shown_info = MagicMock()
    shown_error = MagicMock()
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.showinfo", shown_info)
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.showerror", shown_error)

    screen.macro_buttons[0].cget("command")()

    shown_info.assert_not_called()
    shown_error.assert_called_once_with(
        "Catalyst", "Couldn't apply Main Twitter:\nMissing sheet 'Tags'."
    )


def test_an_error_status_on_a_multi_macro_tasks_second_button_is_handled_the_same_way(
    root, tmp_path, monkeypatch
):
    target_path = tmp_path / "target.xlsx"
    target_path.touch()

    screen = MacroApplierScreen(root, on_back=lambda: None)
    screen.target_path = target_path
    screen.task_dropdown.set("Standard Workflow")
    screen._on_task_selected("Standard Workflow")

    session = MagicMock()
    session.target_path = target_path.resolve()
    session.apply.return_value = ("ERROR", "No target workbook found.")
    monkeypatch.setattr(
        "catalyst.tools.macro_applier.screen.MacroSession", MagicMock(return_value=session)
    )
    shown_error = MagicMock()
    monkeypatch.setattr("catalyst.tools.macro_applier.screen.messagebox.showerror", shown_error)

    screen.macro_buttons[1].cget("command")()

    shown_error.assert_called_once_with(
        "Catalyst", "Couldn't apply Social File Arrangement:\nNo target workbook found."
    )
