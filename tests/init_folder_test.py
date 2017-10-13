''' Unit tests for init folder '''
import os
from unittest import TestCase

import jsonpickle
from nose.tools import assert_equal

from ..folder import init

from .base_test import setup_tmp_dir

def touch(path):
    ''' Touch (create / update modified time) for files '''
    with open(path, 'a'):
        os.utime(path, None)

class InitFolderTest(TestCase):
    ''' Unittest class for init folder '''
    def setUp(self):
        ''' Test setup method '''
        self.tmp_dir, self.source_dir, self.destination_dir = setup_tmp_dir()
        touch(os.path.join(self.source_dir, 'file_1.pdf'))
        touch(os.path.join(self.source_dir, 'file_2.pdf'))
        touch(os.path.join(self.source_dir, 'file_3.pdf'))

    def teardown(self):
        ''' Test teardown method '''
        os.removedirs(self.tmp_dir)

    def test_successful_folder_summary_generation(self):
        ''' Validate init returns folder information '''
        json = init(self.source_dir)
        assert_equal(json, jsonpickle.encode({
            'files': ['file_1.pdf', 'file_2.pdf', 'file_3.pdf'],
            'folders': []
            }))
