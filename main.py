import typer
from rich import print
from rich.prompt import Prompt
from pick import pick
from package_finder import get_parent_package_name
import os

app = typer.Typer()


@app.command()
def gen(name: str = typer.Argument(None, help="Name of the package"),
        all: bool = typer.Option(False, help="Generate all features", allow_dash=False)):
    pick_title = ('Pick features of the module (press SPACE to mark,'
                  ' ENTER to pick all, ENTER  without mark to pick all): ')
    pick_options = ['Controller', 'Service', 'Repository', 'Model', "DTO"]

    try:
        package = get_parent_package_name(os.getcwd())
    except FileNotFoundError:
        print("Could not find java directory upstream.")
        package = None
    parent_package = Prompt.ask("Please enter the name of the parent package", default=package)

    if name is None:
        name = Prompt.ask("Enter the name of the package")
    if all:
        generate(name, pick_options, parent_package)
        return

    selected = [i[0] for i in pick(pick_options, pick_title, indicator="Ɛ>", multiselect=True, min_selection_count=0)]
    if len(selected) == 0:
        generate(name, pick_options, parent_package)
        return
    generate(name, selected, parent_package)


def generate(name: str, features: list[str], parent_package: str):
    print(f"Generating {name} package with a {', '.join(features)} in {name.lower()}")
    if not os.path.exists(f'./{name.lower()}'):
        os.mkdir(f'./{name.lower()}')

    for feature in features:
        with open(f'./templates/{feature.lower()}') as f:
            content = f.read()
        content = (content.replace('{parentPackageName}', parent_package)
                   .replace('{packageName}', name[0].lower() + name[1:])
                   .replace('{capitalizedPackageName}', name.capitalize()))

        with open(f'./{name.lower()}/{feature.lower()}.java', 'w') as f:
            f.write(content)


if __name__ == "__main__":
    app()
