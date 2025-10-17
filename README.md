# Player Control

TODO: Add project description

## Installation

This project uses `uv` for dependency management.

1.  Create a virtual environment:
    ```bash
    uv venv
    ```

2.  Activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```

3.  Install the project in editable mode with development dependencies:
    ```bash
    uv pip install -e .[dev]
    ```

## Global Installation (with pipx)

For a global installation, you can use `pipx` to install the application in an isolated environment. This makes the `player_control` command available anywhere on your system.

```bash
pipx install .
```

## Usage

Once installed, you can run the application from your terminal:

```bash
player_control
```

## Development

To run the tests:

```bash
pytest
```