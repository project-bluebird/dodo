#!/bin/bash
set -ev
if [ $TRAVIS_OS_NAME = "linux" ]; then
    sudo apt-get update
    # Get set up to run jupyter notebooks:
    sudo apt-get install texlive-latex-recommended
    sudo apt-get install texlive-latex-extra
    sudo apt-get install texlive-fonts-recommended
    sudo apt-get install chktex
    sudo apt-get install dvipng
    sudo apt-get install pandoc
    pip install --upgrade jupyter
    pip install nbconvert
    jupyter nbconvert --ExecutePreprocessor.kernel_name=python --ExecutePreprocessor.timeout=600 --to html --execute notebooks/Python-example-notebook.ipynb
    jupyter nbconvert --ExecutePreprocessor.kernel_name=ir --ExecutePreprocessor.timeout=600 --to html --execute notebooks/R-example-notebook.ipynb
fi
