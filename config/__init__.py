import os
import sys
import config.settings

# create settings object corresponding to specified env
APP_ENV = os.environ.get('APP_ENV', 'Dev')
_current = getattr(sys.modules['config.settings'], f'{APP_ENV}Config')()

# copy attributes to the module for convenience
for atr in [f for f in dir(_current) if '__' not in f]:
    # environment can override anything
    val = os.environ.get(atr, getattr(_current, atr))
    setattr(sys.modules[__name__], atr, val)


def as_dict():
    return {atr_: getattr(config, atr_) for atr_ in [f for f in dir(config) if '__' not in f]}


