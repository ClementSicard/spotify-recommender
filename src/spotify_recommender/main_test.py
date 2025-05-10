"""Tests for the main function."""


def test_1() -> None:
    """Test that the main function does not raise an AssertionError."""
    from spotify_recommender.main import main

    main()

    assert True
