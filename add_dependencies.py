import subprocess




def add_dependencies():
    with open("requirements.txt") as f:
        for line in f:
            package = line.strip()
            if package and not package.startswith("#"):
                subprocess.run(["poetry", "add", package])

def add_dependencies_dev():
    with open("requirements-dev.txt") as f:
        for line in f:
            package = line.strip()
            if package and not package.startswith("#"):
                subprocess.run(["poetry", "add", "--dev", package])

if __name__ == "__main__":
    add_dependencies()
