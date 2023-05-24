"""
get config from config.yaml
"""
import yaml

try:
    with open("config.yaml") as f:
        _config = yaml.safe_load(f)
except:
    _config = {}


def config(*keys):
    def safe_get(dct, *keys):
        for key in keys:
            try:
                dct = dct[key]
            except KeyError:
                return None
        return dct

    return safe_get(_config, *keys)
