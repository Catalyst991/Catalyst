from catalyst.tools.macro_applier.tasks import TASKS, TALKWALKER_TRADITIONAL


def test_registry_has_the_four_confirmed_tasks_with_correct_macro_order():
    by_name = {task.name: [macro.name for macro in task.macros] for task in TASKS}

    assert [task.name for task in TASKS] == [
        "Standard Workflow",
        "Daily Report Excel File",
        "Traditional Talkwalker",
        "Just Social",
    ]
    assert by_name["Standard Workflow"] == ["Main Twitter", "Social File Arrangement"]
    assert by_name["Daily Report Excel File"] == ["Main Twitter", "Daily Report Formatting"]
    assert by_name["Traditional Talkwalker"] == ["Talkwalker Traditional"]
    assert by_name["Just Social"] == ["Main Twitter"]


def test_every_macro_resolves_to_its_bundled_xlsm_file_on_disk():
    for task in TASKS:
        for macro in task.macros:
            assert macro.path.exists(), f"{macro.path} is missing"
            assert macro.path.suffix == ".xlsm"


def test_only_talkwalker_traditional_needs_confirmation():
    for task in TASKS:
        for macro in task.macros:
            assert macro.needs_confirmation == (macro is TALKWALKER_TRADITIONAL)
