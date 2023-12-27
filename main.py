import typer
from rich import print
from rich.prompt import Prompt, Confirm
from pick import pick

from features_list import features_list
from package_finder import try_get_parent_package_name
import os

from utils import abort

app = typer.Typer()


@app.command()
def gen(name: str = typer.Argument(None, help="Name of the package"),
        all: bool = typer.Option(False, help="Generate all features", allow_dash=True)):
    pick_feature_title = ('Pick [green bold]features[/green bold] of the module (press SPACE to mark,'
                          ' ENTER to proceed): ')
    feature_options = list(features_list.keys())  # TODO DTO, Mapper, etc.

    parent_package = get_parent_package_name()
    name = get_new_package_name(name)

    if all:
        generate_features(name, feature_options, parent_package)
        return

    selected = [i[0] for i in
                pick(feature_options, pick_feature_title, indicator="Ɛ>", multiselect=True, min_selection_count=0)]
    if len(selected) == 0:
        print("No features selected.")
        abort()
    generate_features(name, selected, parent_package)


def get_new_package_name(name):
    if name is None:
        name = Prompt.ask("Enter the name of the [green bold]new[/ green bold] package")
    if not name:
        print("Name of the package cannot be empty.")
        abort()
    return name


def get_parent_package_name():
    parent_package = None
    try:
        parent_package = try_get_parent_package_name(os.getcwd())
    except FileNotFoundError:
        print(
            "Could not find [red]java[/red] directory upstream."
            " Please generate the package under the [red]java[/red] directory.")
        abort()
    parent_package = Prompt.ask(
        "Please enter the name of the [green bold]parent[/green bold] package. Press ENTER for",
        default=parent_package)
    return parent_package


def generate_features(name: str, features: list[str], parent_package: str):
    print(f"Generating [green bold]{name}[/green bold] package with a {', '.join(features)}")
    if not os.path.exists(f'./{name.lower()}'):
        os.mkdir(f'./{name.lower()}')

    for feature in features:
        template = features_list[feature]
        content = parse_template(template, name, parent_package)

        if feature == 'Model':
            file_name = f'{name.capitalize()}.java'
        else:
            file_name = f'{name.capitalize()}{feature}.java'
        with open(f'./{name.lower()}/{file_name}', 'w') as f:
            f.write(content)


def parse_template(content, name, parent_package):
    content = (content.replace('{parentPackageName}', parent_package)
               .replace('{packageName}', name[0].lower() + name[1:])
               .replace('{capitalizedPackageName}', name.capitalize()))
    return content


if __name__ == "__main__":
    app()
