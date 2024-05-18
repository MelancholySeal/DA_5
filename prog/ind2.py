import os
import argparse
from pathlib import Path


def display_tree(directory, level, max_level, include_files, show_hidden, show_sizes):
    def format_size(size):
        # Convert size to human-readable format
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.2f}{unit}"
            size /= 1024
        return f"{size:.2f}PB"

    def tree(dir_path, prefix=""):
        if max_level is not None and level[0] >= max_level:
            return
        level[0] += 1

        contents = sorted(list(dir_path.iterdir()), key=lambda p: p.is_file())
        for count, path in enumerate(contents):
            if not show_hidden and path.name.startswith("."):
                continue

            connector = "└── " if count == len(contents) - 1 else "├── "
            size_info = (
                f" ({format_size(path.stat().st_size)})"
                if show_sizes and path.is_file()
                else ""
            )
            print(f"{prefix}{connector}{path.name}{size_info}")

            if path.is_dir():
                extension = "    " if count == len(contents) - 1 else "│   "
                tree(path, prefix + extension)

        level[0] -= 1

    start_path = Path(directory).expanduser()
    if not start_path.exists():
        print(f"Directory '{directory}' does not exist.")
        return

    print(start_path)
    tree(start_path)


def main():
    parser = argparse.ArgumentParser(
        description="Display a tree structure of directories."
    )
    parser.add_argument(
        "directory", nargs="?", default=".", help="The directory to list."
    )
    parser.add_argument(
        "-L", "--level", type=int, help="Descend only level directories deep."
    )
    parser.add_argument(
        "-f", "--files", action="store_true", help="Include files in the listing."
    )
    parser.add_argument(
        "-a", "--all", action="store_true", help="Include hidden files and directories."
    )
    parser.add_argument("-s", "--sizes", action="store_true", help="Show file sizes.")
    parser.add_argument(
        "-c",
        "--count",
        action="store_true",
        help="Show count of files and directories.",
    )

    args = parser.parse_args()

    if args.count:
        count_files_and_dirs(args.directory)
    else:
        display_tree(args.directory, [0], args.level, args.files, args.all, args.sizes)


def count_files_and_dirs(directory):
    total_files = 0
    total_dirs = 0

    for root, dirs, files in os.walk(directory):
        total_dirs += len(dirs)
        total_files += len(files)

    print(f"Total directories: {total_dirs}")
    print(f"Total files: {total_files}")


if __name__ == "__main__":
    main()
