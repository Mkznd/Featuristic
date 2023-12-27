import os


def get_parent_package_name(start: str):
    target = "java"
    path = start
    pack = []
    i = 0
    while i < 10:
        current = os.path.basename(path)
        if current == target:
            return ".".join(pack[::-1])
        pack.append(current)
        path = os.path.dirname(path)
        i += 1
    raise FileNotFoundError("Could not find java package")
