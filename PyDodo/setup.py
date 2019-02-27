from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    REQUIRED_PACKAGES = f.read().splitlines()

setup(
    name = "PyDodo",
    description = "Scaffold for ATC agents to interface with the BlueBird API",
    version = "0.1.0",
    author = "Radka Jersakova and Ruairidh MacLeod",
    install_requires=REQUIRED_PACKAGES,
    packages = ["pydodo"],
    # packages = find_packages(exclude=['*test']),
    url="https://github.com/alan-turing-institute/dodo/PyDoDo"
)
