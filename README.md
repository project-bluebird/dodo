# dodo

Scaffold for ATC agents

## PyDodo

### Dev install

```{bash}
git clone https://github.com/alan-turing-institute/dodo.git
cd dodo/Pydodo
```
For developing use either one of:

```{bash}
python setup.py develop
pip install -e .
```

This does not install the package but creates a .egg-link directory relative to the project path.

To install the pacakge in the user site-packages directory use either of:

```{bash}
python setup.py install
pip install .
```

### GitHub install

TO DO

### Example usage

```{python}
import pydodo

pydodo.reset_simulation()
```
