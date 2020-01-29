import os
import wget

from setuptools import setup
from setuptools.command.develop import develop as _develop
from setuptools.command.install import install as _install

with open("requirements.txt", "r") as f:
    REQUIRED_PACKAGES = f.read().splitlines()


def get_config(config_dir=None):
    """Downloads config file from GitHub and saves it in config_dir."""
    print("Getting the config file")
    config_url = (
        "https://raw.githubusercontent.com/alan-turing-institute/dodo/master/config.yml"
    )
    if config_dir == None:
        this_dir, this_filename = os.path.split(os.path.abspath(__file__))
        config_dir = os.path.join(this_dir, "pydodo")
    wget.download(config_url, config_dir)


class develop(_develop):
    """Post-installation in develop mode"""

    def run(self):
        _develop.run(self)
        this_dir, this_filename = os.path.split(os.path.abspath(__file__))
        config_dir = os.path.join(this_dir, "pydodo")
        if not os.path.exists(os.path.join(config_dir, "config.yml")):
            get_config()


class install(_install):
    """Post-installation in install mode"""

    def run(self):
        _install.run(self)
        package_path = os.path.join(self.install_lib, "pydodo")
        if not os.path.exists(os.path.join(package_path, "config.yml")):
            self.execute(get_config, (package_path,))


setup(
    name="PyDodo",
    description="Scaffold for ATC agents to interface with the BlueBird API",
    version="0.1.0",
    author="Radka Jersakova and Ruairidh MacLeod",
    install_requires=REQUIRED_PACKAGES,
    packages=["pydodo", "birdhouse"],
    url="https://github.com/alan-turing-institute/dodo/PyDoDo",
    cmdclass={"install": install, "develop": develop},
)
