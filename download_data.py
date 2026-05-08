#!/usr/bin/env python3

import subprocess
from pathlib import Path


def run(command):
    """Run a shell command and stop if it fails."""
    subprocess.run(command, check=True)


def capture(command):
    """Run a shell command and return its stdout."""
    result = subprocess.run(
        command,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return result.stdout


def main():
    gitignore_path = Path(".gitignore")

    print("Fetching latest data branch from origin (your repo)...")
    run(["git", "fetch", "origin", "data"])

    print("Adding data files from origin/data to .gitignore...")

    existing_ignores = set()
    if gitignore_path.exists():
        existing_ignores = {
            line.strip()
            for line in gitignore_path.read_text().splitlines()
            if line.strip()
        }

    files_output = capture(["git", "ls-tree", "-r", "--name-only", "origin/data"])
    data_files = [line.strip() for line in files_output.splitlines() if line.strip()]

    with gitignore_path.open("a", newline="\n") as gitignore:
        for file in data_files:
            if file not in existing_ignores:
                gitignore.write(file + "\n")
                existing_ignores.add(file)
                print(f"Adding: {file}")

    print("Pulling files from origin/data...")
    run(["git", "checkout", "origin/data", "--", "."])

    run(["git", "restore", "--staged", "."])

    print("\033[92m\nData successfully pulled!\n\033[0m")


if __name__ == "__main__":
    main()