from pathlib import Path
import os

ROOT_DIRECTORY = Path(__file__).parent.parent.parent.parent

def find_file(searched_file: str):
    for root, dirs, files in os.walk(ROOT_DIRECTORY, topdown=True):
        dirs[:] = [dir for dir in dirs if dir != ".venv"]
        for name in files:
            if name == searched_file:
                return os.path.join(root, name)


if __name__ == "__main__":
    print(find_file("query.py"))