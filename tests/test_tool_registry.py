from catalyst.tool_registry import build_registry


def test_registry_lists_daily_report_generator_tool():
    sentinel = lambda: None

    tools = build_registry(daily_report_open=sentinel)

    assert len(tools) == 1
    assert tools[0].name == "Daily Report Generator"
    assert tools[0].open is sentinel
