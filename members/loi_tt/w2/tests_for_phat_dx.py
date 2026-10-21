import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from members.khanh_np.w1 import grades, rules, text_tools, timetable, translate  # noqa: E402


# --- W1-1: grades.summary -------------------------------------------------


def test_summary_even_count_uses_midpoint():
    """Median of an even-length list is the mean of the two middle values."""
    assert grades.summary([2, 8])["median"] == 5.0
    assert grades.summary([1, 2])["median"] == 1.5


def test_summary_does_not_mutate_its_argument():
    scores = [9, 3, 7]
    grades.summary(scores)
    assert scores == [9, 3, 7]


# --- W1-2: text_tools -----------------------------------------------------


def test_word_count_lowercases_alphanumeric_tokens():
    assert text_tools.word_count("CSC10014 csc10014 CSC10014") == {"csc10014": 3}


def test_top_k_returns_everything_when_k_exceeds_vocabulary():
    assert text_tools.top_k("b a c", 10) == [("a", 1), ("b", 1), ("c", 1)]
    assert text_tools.top_k("a b", 0) == []


def test_word_count_edge_case_punctuation_only_text():
    """EDGE CASE not covered by tests/test_w1.py: text that contains no word."""
    assert text_tools.word_count("... !!! ;;;") == {}
    assert text_tools.top_k("... !!!", 3) == []


# --- W1-3: rules ----------------------------------------------------------


def test_can_register_thesis_is_strict_on_both_limits():
    assert rules.can_register_thesis(120, 2.0)  # exact boundary is accepted
    assert not rules.can_register_thesis(119, 4.0)  # one credit short
    assert not rules.can_register_thesis(150, 1.99)  # GPA just below the limit


def test_missing_reports_the_gpa_gap_message():
    assert rules.missing(120, 1.5) == ["need 0.5 higher GPA"]
    assert rules.missing(100, 1.5) == [
        "need 20 more credits",
        "need 0.5 higher GPA",
    ]


@pytest.mark.xfail(
    strict=True,
    reason="2.0 - 1.998 rounds to 0.0, so the message becomes 'need 0 higher GPA'",
)
def test_missing_reports_a_sub_hundredth_gpa_gap():
    """EDGE CASE not covered by tests/test_w1.py: a GPA gap below 0.01 points."""
    assert rules.missing(120, 1.998) == ["need 0.002 higher GPA"]


# --- W1-4: translate.binary_search ----------------------------------------


def test_binary_search_hits_first_and_last_index():
    assert translate.binary_search([1, 3, 5, 7], 1) == 0
    assert translate.binary_search([1, 3, 5, 7], 7) == 3
    assert translate.binary_search([42], 42) == 0
    assert translate.binary_search([42], 41) == -1


# --- W1-5: timetable.by_day -----------------------------------------------


def test_by_day_keeps_duplicates_and_separate_day_spellings():
    pairs = [("CSC10014", "Mon"), ("CSC10014", "Mon"), ("MTH00003", "mon")]
    assert timetable.by_day(pairs) == {
        "Mon": ["CSC10014", "CSC10014"],
        "mon": ["MTH00003"],
    }
    assert timetable.by_day([("CSC10001", "Wed")]) == {"Wed": ["CSC10001"]}
