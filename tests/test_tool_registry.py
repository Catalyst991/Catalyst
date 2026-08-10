from catalyst.tool_registry import build_registry


def test_registry_lists_daily_report_generator_tool():
    sentinel = lambda: None

    tools = build_registry(daily_report_open=sentinel, macro_applier_open=lambda: None)

    assert tools[0].name == "Daily Report Generator"
    assert tools[0].open is sentinel


def test_registry_lists_macro_applier_tool():
    sentinel = lambda: None

    tools = build_registry(daily_report_open=lambda: None, macro_applier_open=sentinel)

    assert len(tools) == 2
    assert tools[1].name == "Macro Applier"
    assert tools[1].open is sentinel
