"""W2-4: Tran Phuc Khanh tests Nguyen Phuc Khanh's W1 binary search."""
from members.khanh_np.w1.translate import binary_search


def test_existing_positions():
    values = [1, 3, 5, 7, 9]
    assert binary_search(values, 1) == 0
    assert binary_search(values, 5) == 2
    assert binary_search(values, 9) == 4


def test_missing_key():
    assert binary_search([1, 3, 5, 7], 4) == -1
    assert binary_search([1, 3, 5, 7], 10) == -1


def test_empty_list():
    assert binary_search([], 1) == -1


def test_single_element():
    assert binary_search([7], 7) == 0
    assert binary_search([7], 6) == -1


def test_duplicate_values():
    # Edge case absent from instructor tests: any matching index is valid.
    values = [1, 3, 3, 3, 5]
    index = binary_search(values, 3)
    assert index in {1, 2, 3}
    assert values[index] == 3
