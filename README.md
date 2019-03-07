# dodo

Scaffold for ATC agents

## PyDodo

### Testing

```{bash}
git clone https://github.com/alan-turing-institute/dodo.git
cd dodo/PyDodo
pytest -v
```

If BlueSky and BlueBird are not running, the integration tests are skipped.

### Install

1. From local

```{bash}
git clone https://github.com/alan-turing-institute/dodo.git
cd dodo/Pydodo
pip install .
```

2. From GitHub

```
pip install git+https://github.com/alan-turing-institute/dodo.git@py_dodo#egg=pydodo\&subdirectory=PyDodo
```

### Example usage

```{python}
import pydodo

pydodo.reset_simulation()
```
