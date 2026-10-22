from week01.main import get_repo_stars


def test_stars_is_positive():
    assert get_repo_stars("python", "cpython") > 0