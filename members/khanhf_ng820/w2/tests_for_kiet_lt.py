import pytest

try:
    from members.kiethm07.w1 import grades, rules, text_tools, timetable, translate
except ImportError:
    from members.kiet_lt.w1 import grades, rules, text_tools, timetable, translate


def test_summary_edge_cases() -> None:
    # Identical score list
    assert grades.summary([10.0, 10.0, 10.0]) == {
        "min": 10.0,
        "max": 10.0,
        "mean": 10.0,
        "median": 10.0,
    }
    # Even-length list median calculation
    assert grades.summary([2.0, 4.0]) == {
        "min": 2.0,
        "max": 4.0,
        "mean": 3.0,
        "median": 3.0,
    }
    # Single element list
    assert grades.summary([8.5])["median"] == 8.5
    # Empty list must raise ValueError
    with pytest.raises(ValueError):
        grades.summary([])


def test_word_count_and_top_k_edge_cases() -> None:
    # Multiple punctuations and case normalization
    sample = "Hello, world! Hello: world? Python; fast."
    counts = text_tools.word_count(sample)
    assert counts["hello"] == 2
    assert counts["world"] == 2
    assert counts["python"] == 1
    assert counts["fast"] == 1

    # Tie-breaking sorted alphabetically ascending
    tie_text = "zebra apple zebra apple banana"
    # counts: zebra: 2, apple: 2, banana: 1 -> top 2 must break ties alphabetically: apple then zebra
    assert text_tools.top_k(tie_text, 2) == [("apple", 2), ("zebra", 2)]

    # Empty string or non-positive k
    assert text_tools.top_k("", 3) == []
    assert text_tools.top_k("word count", 0) == []


def test_thesis_rules_edge_cases() -> None:
    # Exact threshold boundary
    assert rules.can_register_thesis(120, 2.0) is True
    assert rules.can_register_thesis(119, 2.0) is False
    assert rules.can_register_thesis(120, 1.99) is False

    # Deficit on both credits and GPA
    reasons = rules.missing(115, 1.8)
    assert "need 5 more credits" in reasons
    assert "need 0.2 more GPA" in reasons
    assert len(reasons) == 2

    # Fully qualified returns empty list
    assert rules.missing(125, 3.5) == []


def test_matrix_transpose_edge_cases() -> None:
    # Rectangular matrix
    assert translate.transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    # Single element matrix
    assert translate.transpose([[99]]) == [[99]]
    # Row vector to column vector
    assert translate.transpose([[1, 2, 3]]) == [[1], [2], [3]]
    # Column vector to row vector
    assert translate.transpose([[1], [2], [3]]) == [[1, 2, 3]]
    # Empty matrix and empty row
    assert translate.transpose([]) == []
    assert translate.transpose([[]]) == []


def test_timetable_by_day_edge_cases() -> None:
    # Multiple courses on same day sorted alphabetically
    schedule = [
        ("CS252", "Mon"),
        ("CS101", "Mon"),
        ("MA101", "Tue"),
        ("CS100", "Mon"),
    ]
    expected = {
        "Mon": ["CS100", "CS101", "CS252"],
        "Tue": ["MA101"],
    }
    assert timetable.by_day(schedule) == expected

    # Empty schedule returns empty dictionary
    assert timetable.by_day([]) == {}
