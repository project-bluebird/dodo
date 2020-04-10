# Dodo

[![Build Status](https://travis-ci.com/alan-turing-institute/dodo.svg?branch=master)](https://travis-ci.com/alan-turing-institute/dodo)

## Overview

Dodo is a package that provides a scaffold for building air traffic control agents, as part of the [Simurgh](https://github.com/alan-turing-institute/simurgh) project. The packages is written in Python ([PyDodo](#pydodo)) and R ([rdodo](#rdodo)).

Note that the package is built to communicate with **[BlueBird](https://github.com/alan-turing-institute/bluebird) version >= 2.0**.

All the default settings and parameter values (e.g., BlueBird version number) are specified in a common [configuration file](config.yml).

For an overview of all functionality, please read the [specification](Specification.md) document.

### Contents

* [Pydodo](#pydodo)
  * [Installation](#pydodo-installation)
  * [Usage](#pydodo-usage)
  * [Development](#pydodo-development)
* [rdodo](#rdodo)
  * [Installation](#rdodo-installation)
  * [Usage](#rdodo-usage)
  * [Development](#rdodo-development)
* [Contributing](#contributing)

## PyDodo

### PyDodo installation

(Optional first step)

```
conda create -n pydodo python=3.7
conda activate pydodo
```
...
```{bash}
git clone https://github.com/alan-turing-institute/dodo.git
cd dodo/PyDodo
pip install .
```

### PyDodo usage

If BlueBird (and a simulator) are running, then one can communicate with BlueBird using PyDodo. For example:

 ```python
 >>> import pydodo
 >>>
 >>> pydodo.reset_simulation()
 True
 >>>
 ```

The [specification document](https://github.com/alan-turing-institute/dodo/blob/master/Specification.md) gives a detailed overview of the supported commands.

See the [example notebook](https://github.com/alan-turing-institute/simurgh/blob/master/examples/Example-pipeline.ipynb) in the Simurgh project repository for a run through of how to use PyDodo to interact with BlueBird.

### PyDodo development

#### Tests

Run the tests from the project root:

```
pytest PyDodo/
```

If BlueSky and BlueBird are running and PyDodo can connect to them, all tests are run.
Otherwise integration tests are skipped and only unit tests are run.

#### Style guide

Docstrings should follow [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) convention.
We encourage extensive documentation.

The python code itself should follow [PEP8](https://www.python.org/dev/peps/pep-0008/) convention whenever possible, with at most about 500 lines of code (not including docstrings) per script.

To format the code we recommend using the [black](https://black.readthedocs.io/en/stable/) code formatter.

## rdodo

### rdodo installation

### rdodo usage

### rdodo development

## Contributing

If you have any questions that aren't discussed here, please let us know by opening an [issue](https://github.com/alan-turing-institute/dodo/issues).

We welcome all contributions from documentation to testing to writing code. Don't let trying to be perfect get in the way of being good - exciting ideas are more important than perfect pull requests.

To contribute to PyDodo or rdodo development, please check the corresponding section ([PyDodo development](#pydodo-development) or [rdodo development](#rdodo-development) for details.

To implement Dodo in another programming language, please follow the [specification](Specification.md) document. The shared [configuration file](config.yml) specifies common required parameters and settings.
