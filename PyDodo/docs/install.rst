**********************
    Installation
**********************


1. From local::

    git clone https://github.com/alan-turing-institute/dodo.git
    cd dodo/Pydodo
    pip install .

.. runblock:: console

    $ cat ../requirements.txt

2. From GitHub::

    pip install git+https://github.com/alan-turing-institute/dodo.git@py_dodo#egg=pydodo\&subdirectory=PyDodo

Example usage::

>>> import pydodo
>>> pydodo.reset_simulation()
