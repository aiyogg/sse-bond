"""
get config from config.yaml
"""
import yaml

# href="//static.sse.com.cn/bond/bridge/information/c/202303/917b7ac761c64019b7fdd867481bb461.pdf"
SSE_BOND_STATIC_URL = "http://static.sse.com.cn/bond"

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
