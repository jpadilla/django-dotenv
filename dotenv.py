import os
import re
import sys
import warnings

def read_dotenv(dotenv=None):
    """
    Read a .env file into os.environ.

    If not given a path to a dotenv path, does filthy magic stack backtracking
    to find manage.py and then find the dotenv.
    """
    if dotenv is None:
        frame = sys._getframe()
        dotenv = os.path.join(os.path.dirname(frame.f_back.f_code.co_filename), '.env')
        if not os.path.exists(dotenv):
            warnings.warn("not reading %s - it doesn't exist." % dotenv)
            return
    for k, v in parse_dotenv(dotenv):
        os.environ.setdefault(k, v)

def parse_dotenv(dotenv):
    for line in open(dotenv):
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue

        # https://gist.github.com/bennylope/2999704
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if not m1:
            continue
        key, val = m1.group(1), m1.group(2)
        m2 = re.match(r"\A'(.*)'\Z", val)
        if m2:
            val = m2.group(1)
        else:
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
        yield key, val
