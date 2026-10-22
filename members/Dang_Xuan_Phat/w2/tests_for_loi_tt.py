try:
    from members.TranThanhLoi27.w1.translate import insertion_sort
except ModuleNotFoundError:
    from members.loi_tt.w1.translate import insertion_sort


def test_empty_and_single_element():
    assert insertion_sort([]) == []
    assert insertion_sort([42]) == [42]


def test_already_sorted():
    data = [1, 2, 3, 4, 5, 6]
    assert insertion_sort(data) == [1, 2, 3, 4, 5, 6]


def test_reverse_sorted():
    data = [9, 7, 5, 3, 1]
    assert insertion_sort(data) == [1, 3, 5, 7, 9]


def test_duplicate_and_identical_elements():
    assert insertion_sort([5, 5, 5, 5]) == [5, 5, 5, 5]
    assert insertion_sort([4, 2, 5, 2, 1, 4]) == [1, 2, 2, 4, 4, 5]


def test_negative_and_zero_values():
    data = [-3, 0, -10, 5, -1]
    assert insertion_sort(data) == [-10, -3, -1, 0, 5]


def test_in_place_mutation():
    original = [3, 1, 2]
    returned = insertion_sort(original)
    assert returned is original
    assert original == [1, 2, 3]


def test_large_array():
    data = list(range(100, 0, -1))
    expected = list(range(1, 101))
    assert insertion_sort(data) == expected
