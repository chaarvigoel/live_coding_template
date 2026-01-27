import argparse
import sys

try:
    from .utils import parse_config  # When run as module: python -m src.main
except ImportError:
    from utils import parse_config  # When run directly or via pytest with pythonpath


def greet(name: str) -> str:
    return f"Hello, {name}!"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Live coding template CLI")
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to config JSON file (default: config.json)",
    )
    args = parser.parse_args(argv)

    print(greet("World"))
    config = parse_config(args.config)
    if "message" in config:
        print(config["message"])
    print("Template ready")


if __name__ == "__main__":
    main()
