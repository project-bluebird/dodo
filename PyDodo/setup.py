import os
from setuptools import setup, find_packages
from setuptools.command.develop import develop as _develop
from setuptools.command.install import install as _install
from subprocess import call

# BASEPATH = os.path.dirname(os.path.abspath(__file__))

with open("requirements.txt", "r") as f:
    REQUIRED_PACKAGES = f.read().splitlines()

def get_config():
    print("Getting the config file")
    config = 'https://raw.githubusercontent.com/alan-turing-institute/dodo/master/config.yml'
    call(['wget', config])

class develop(_develop):
    """Post-installation in develop mode"""
    def run(self):
        _develop.run(self)
        get_config()

class install(_install):
    """Post-installation in install mode"""
    def run(self):
        _install.run(self)
        get_config()

setup(
    name = "PyDodo",
    description = "Scaffold for ATC agents to interface with the BlueBird API",
    version = "0.1.0",
    author = "Radka Jersakova and Ruairidh MacLeod",
    install_requires=REQUIRED_PACKAGES,
    packages = ["pydodo"],
    # packages = find_packages(exclude=['*test']),
    url="https://github.com/alan-turing-institute/dodo/PyDoDo",
    cmdclass={"install": install, "develop": develop}
)
