import os
from setuptools import setup, find_packages
from setuptools.command.install import _install
from subprocess import call

# BASEPATH = os.path.dirname(os.path.abspath(__file__))

with open("requirements.txt", "r") as f:
    REQUIRED_PACKAGES = f.read().splitlines()

class install(_install):
    def run(self):
        _install.run(self)
        print("Getting the config file")
        call(['wget', 'https://raw.githubusercontent.com/alan-turing-institute/dodo/master/config.yml'])

setup(
    name = "PyDodo",
    description = "Scaffold for ATC agents to interface with the BlueBird API",
    version = "0.1.0",
    author = "Radka Jersakova and Ruairidh MacLeod",
    install_requires=REQUIRED_PACKAGES,
    packages = ["pydodo"],
    # packages = find_packages(exclude=['*test']),
    url="https://github.com/alan-turing-institute/dodo/PyDoDo",
    cmdclass={"install": install}
)
