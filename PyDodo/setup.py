import os
from setuptools import setup, find_packages
from setuptools.command.develop import develop as _develop
from setuptools.command.install import install as _install
from subprocess import call

with open("requirements.txt", "r") as f:
    REQUIRED_PACKAGES = f.read().splitlines()


def get_config(dir=None):
    """
    Downloads config file from GitHub and saves it in dir
    (using either wget or curl).
    """
    print("Getting the config file")
    config = (
        "https://raw.githubusercontent.com/alan-turing-institute/dodo/master/config.yml"
    )
    cmd = ["wget", config, "2>/dev/null", "||", " curl", "-O", config]
    if dir == None:
        call(cmd)
    else:
        # call(["wget", config], cwd=dir)
        call(cmd, cwd=dir)


class develop(_develop):
    """Post-installation in develop mode"""

    def run(self):
        _develop.run(self)
        if not os.path.exists("config.yml"):
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
    packages=["pydodo"],
    # packages = find_packages(exclude=['*test']),
    url="https://github.com/alan-turing-institute/dodo/PyDoDo",
    cmdclass={"install": install, "develop": develop},
)
