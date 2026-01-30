from pathlib import Path
from typing import List

def name_cleaner(file_path: str):


    path = Path(file_path)
    names = set()
    duplicates = []
    invalid = []


    with path.open(encoding="utf-8") as f:

        for line in f:
            name = line.strip().lower()
            if not name.isalpha():
                invalid.append(name)
            elif name in names:
                duplicates.append(name)
            else:
                names.add(name)
    print("The final list of names is", names)
    print("The invalid names were:", invalid)
    print("The duplicate names were:", duplicates)
    





def main():
    print("name_cleaner ready")
    # Resolve path relative to this script (works from any cwd)
    _dir = Path(__file__).resolve().parent.parent
    name_cleaner(str(_dir / "names.txt"))


if __name__ == "__main__":
    main()

