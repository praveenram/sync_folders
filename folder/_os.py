''' Wrapper methods for os functions '''

from stat import S_ISDIR, S_ISREG
import os

def is_directory(stat):
    return S_ISDIR(stat.mode)

def is_file(stat):
    return S_ISREG(stat.mode)

def valid_symlink(path):
    target_path = os.readlink(path)
    # Resolve relative symlinks
    if not os.path.isabs(target_path):
        target_path = os.path.join(os.path.dirname(path), target_path)
    if not os.path.exists(target_path):
        return False
    return True

class Stat(object):
    def __init__(self, path):
        self.stat = os.stat(path)

    @property
    def mode(self):
        return self.stat.st_mode

    @property
    def timestamps(self):
        return [self.stat.st_ctime, self.stat.st_mtime, self.stat.st_atime]

    @property
    def size(self):
        return self.stat.st_size
