''' Shared helpers for tests '''

import os
import uuid
from nose.tools import assert_equal

def setup_tmp_dir():
    ''' Create temporary directory for tests '''
    tmp_dir = '/tmp/tmp-%s' % (uuid.uuid4().hex)
    source_dir = os.path.join(tmp_dir, 'source')
    destination_dir = os.path.join(tmp_dir, 'destination')
    os.makedirs(source_dir)
    os.makedirs(destination_dir)
    return tmp_dir, source_dir, destination_dir

def touch(path, time=None):
    ''' Touch (create / update modified time) for files '''
    with open(path, 'a'):
        os.utime(path, time)

def assert_fixes():
    assert_equal.__self__.maxDiff = None
