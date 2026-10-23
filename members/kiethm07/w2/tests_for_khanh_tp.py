"""W2-4: Cross-member tests for Tran Phuc Khanh's merge_sorted."""

try:
    from members.TranPhucKhanhh.w1.translate import merge_sorted
except (ImportError, AttributeError):
    try:
        from members.TranPhucKhanhh.w1.merge import merge_sorted
    except (ImportError, AttributeError):
        try:
            from members.TranPhucKhanhh.w1.merge import merge_sort as merge_sorted
        except (ImportError, AttributeError):
            from members.khanh_tp.w1.merge import merge_sort as merge_sorted


def test_merge_sorted_normal():
    """Merge two standard sorted lists."""
    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]


def test_merge_sorted_empty_lists():
    """Merge with one or both lists empty."""
    assert merge_sorted([], []) == []
    assert merge_sorted([], [1, 2, 3]) == [1, 2, 3]
    assert merge_sorted([1, 2, 3], []) == [1, 2, 3]


def test_merge_sorted_different_lengths():
    """Merge lists of unequal lengths."""
    assert merge_sorted([1], [2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert merge_sorted([1, 2, 3, 4, 5], [6]) == [1, 2, 3, 4, 5, 6]


def test_merge_sorted_duplicates():
    """Merge lists with duplicate elements."""
    assert merge_sorted([1, 2, 2, 3], [2, 3, 4]) == [1, 2, 2, 2, 3, 3, 4]
    assert merge_sorted([5, 5], [5, 5]) == [5, 5, 5, 5]


def test_merge_sorted_negative_and_zero():
    """Merge lists containing negative numbers and zero."""
    assert merge_sorted([-5, -3, 0], [-4, -1, 2]) == [-5, -4, -3, -1, 0, 2]


def test_merge_sorted_disjoint_ranges():
    """Merge when all elements of one list are smaller than the other."""
    assert merge_sorted([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge_sorted([4, 5, 6], [1, 2, 3]) == [1, 2, 3, 4, 5, 6]


def test_merge_sorted_single_elements():
    """Merge single-element lists."""
    assert merge_sorted([2], [1]) == [1, 2]
    assert merge_sorted([1], [1]) == [1, 1]


def test_merge_sorted_does_not_modify_inputs():
    """Ensure original input lists are not mutated."""
    list_a = [1, 3, 5]
    list_b = [2, 4, 6]
    result = merge_sorted(list_a, list_b)

    assert result == [1, 2, 3, 4, 5, 6]
    assert list_a == [1, 3, 5]
    assert list_b == [2, 4, 6]
