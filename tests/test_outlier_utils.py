from outlier_utils import detect_outliers, modified_z_scores


def test_modified_z_scores_empty():
    assert modified_z_scores([]) == []


def test_modified_z_scores_constant_values():
    scores = modified_z_scores([5.0, 5.0, 5.0])
    assert scores == [0.0, 0.0, 0.0]


def test_detect_outliers_flags_extreme_value():
    values = [10, 12, 12, 13, 12, 11, 12, 100]
    flags = detect_outliers(values, threshold=3.5)
    assert flags == [False, False, False, False, False, False, False, True]


def test_detect_outliers_threshold_customization():
    values = [0, 0, 0, 1]
    flags = detect_outliers(values, threshold=0.1)
    assert flags == [False, False, False, True]
