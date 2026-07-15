import pytest

from awardhawk import combiner


def test_compute_ranked_option_not_implemented_yet():
    with pytest.raises(NotImplementedError):
        combiner.compute_ranked_option(None, None, None, 0.0)
