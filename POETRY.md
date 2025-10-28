# Poetry Migration

This project uses [Poetry](https://python-poetry.org/) for dependency management.

## Setup

Install Poetry:
```bash
pip install poetry
```

Install dependencies:
```bash
poetry install
```

## Development

Run commands in the Poetry environment:
```bash
poetry run python PortMaster/pugwash
poetry run python -m unittest discover tests
```

Or activate the virtual environment:
```bash
poetry shell
python PortMaster/pugwash
```

## Adding Dependencies

Add a production dependency:
```bash
poetry add package-name==version
```

Add a development dependency:
```bash
poetry add --group dev package-name
```

## Building Releases

The `do_release.sh` script automatically:
1. Reads dependencies from `pyproject.toml`
2. Generates a requirements file
3. Downloads dependencies to `PortMaster/deps/`
4. Packages everything into `pylibs.zip`

Dependencies are shipped in the `.zip` archive and loaded at runtime from the `deps/` folder.

## Migration from requirements.txt

Poetry replaces the previous `requirements.txt` approach. All dependencies are now managed in `pyproject.toml` with exact versions and proper dependency resolution via `poetry.lock`.
