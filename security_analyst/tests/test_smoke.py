"""Smoke tests."""


def test_import():
    """Application can be imported."""
    from main import main  # pyright: ignore[reportMissingImports]
    assert callable(main)


def test_main_runs():
    """main() runs without error."""
    from main import main  # pyright: ignore[reportMissingImports]
    main()
