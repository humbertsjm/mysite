Setup project
> Assuming python and pip are alredy installed (see `.python-version` file)

Install `pipenv` (skip if aready installed)

```
pip install pipenv
```

Create an empty `.venv` directory, virtual environtment files will be save there if present

This make easier to set interpeter for vscode configuration

```
mkdir .venv
```

Install packages
```
pipenv install
```

Activate environtment
```
pipenv shell
```