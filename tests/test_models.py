import models
import pytest

mean_test_data = [([1, 2, 3], 2), ([2], 2), ([502, 1000, 4], 502), ([1, 2, 3, 4, 5, 700, 800, 1000], 314.375)]
median_test_data = [([1, 2, 3], 2), ([2], 2), ([1, 22, 23, 24, 25, 26, 1000], 24)]

@pytest.mark.parametrize('numbers,mean', mean_test_data)
def test_mean(numbers, mean):
    assert models.mean(numbers) == mean

@pytest.mark.parametrize('numbers,median', median_test_data)
def test_median(numbers, median):
    assert models.median(numbers) == median
