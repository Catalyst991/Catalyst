from catalyst.tools.daily_report.truncate import truncate


def test_truncates_comment_longer_than_90_chars():
    long_comment = "a" * 91

    result = truncate(long_comment, 90)

    assert result == ("a" * 90) + "..."


def test_leaves_comment_of_90_chars_or_fewer_unchanged():
    short_comment = "a" * 90

    result = truncate(short_comment, 90)

    assert result == short_comment
