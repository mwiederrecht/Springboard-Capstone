from datetime import datetime

def get_timestring():
    now = datetime.now()
    timeString = now.strftime("%Y%m%d%H%M%S%f")
    return timeString

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
