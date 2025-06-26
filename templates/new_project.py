import os
from pathlib import Path
import shutil
import re

def ask_project_type():
    print("Select the template you want to use:")
    print("1. Test template")
    print("2. Experiment template")
    while True:
        choice = input("Enter the number [1/2]: ").strip()
        if choice == "1":
            return "test", "project_template"
        elif choice == "2":
            return "experiments", "project_template"
        else:
            print("Invalid input. Please enter 1 or 2.")

def get_next_project_name(base_dir: Path, prefix: str) -> str:
    base_dir.mkdir(exist_ok=True)
    existing = [p.name for p in base_dir.iterdir()
                if p.is_dir() and re.fullmatch(f"{prefix}[0-9]+", p.name)]
    numbers = [int(name[len(prefix):]) for name in existing]
    next_number = max(numbers, default=0) + 1
    return f"{prefix}{next_number:02d}"

def create_project():
    target_root_name, template_folder_name = ask_project_type()

    project_root = Path(__file__).parent.parent / target_root_name
    template_dir = Path(__file__).parent / template_folder_name

    prefix = "test" if target_root_name == "test" else "exp"
    project_name = get_next_project_name(project_root, prefix)
    target = project_root / project_name

    shutil.copytree(template_dir, target)
    print(f"[INFO] Created new project at: {target}")

if __name__ == "__main__":
    create_project()
