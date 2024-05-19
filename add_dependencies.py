import argparse
import shutil
import subprocess


def add_dependencies(dev: bool):
    requirements_file = "requirements-dev.txt" if dev else "requirements.txt"

    poetry_path = shutil.which("poetry")
    if poetry_path is None:
        raise RuntimeError("Poetry executable not found")

    with open(requirements_file) as f:
        for line in f:
            package = line.strip()
            if package and not package.startswith("#"):
                command = [poetry_path, "add"]
                if dev:
                    command.append("--dev")
                command.append(package)
                subprocess.run(command, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add dependencies using Poetry."
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Use requirements-dev.txt and add dependencies as dev dependencies.",
    )
    args = parser.parse_args()

    add_dependencies(dev=args.dev)
