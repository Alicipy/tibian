import datetime

# Some default values to get back, can be changed for default values

_DAY = datetime.date.today() + datetime.timedelta(days=0)
_STD_CONFIG_FILEPATH = "./config.yaml"

# Some functions to get values from default values
# These functions are meant to be mocked in code


def get_today():
    return _DAY


def get_std_config_filepath():
    return _STD_CONFIG_FILEPATH
