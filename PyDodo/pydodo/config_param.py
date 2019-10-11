from os.path import abspath, dirname, join, exists
import yaml


def find_config():
    """
    Return the default config file location. Normally this is the package
    installation directory, expect when install in develop mode or using pytest.
    If in develop mode, the config file is in the package source root. If using
    pytest, the config file is in the project root.
    """
    config_filename = "config.yml"
    this_dir = dirname(abspath(__file__))
    source_root_dir = dirname(this_dir)
    project_root_dir = dirname(source_root_dir)

    if exists(join(this_dir, config_filename)):
        cfg_file = join(this_dir, config_filename)
    elif exists(join(source_root_dir, config_filename)):
        cfg_file = join(source_root_dir, config_filename)
    elif exists(join(project_root_dir, config_filename)):
        cfg_file = join(project_root_dir, config_filename)
    else:
        raise FileNotFoundError("The config file is missing.")

    return cfg_file


def config_param(param, config="default", cfg_file=find_config()):
    """
    Get a configuration parameter.

    Parameters
    ----------
    param : str
        The name of the config parameter.
    config : str, optional
        The key indicating which configuration parameters to retrieve (e.g., "default").
    cfg_file : str, optional
        The configuration file to read from.

    Returns
    -------
    The value of the requested configuration parameter. An error is thrown if
    the given parameter name is not found in the config file.
    """
    with open(cfg_file) as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    assert param in cfg[config], "Config parameter {} not found".format(param)

    return cfg[config][param]
