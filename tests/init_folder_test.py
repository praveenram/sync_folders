''' Unit tests for folder summary_json '''
import os
from unittest import TestCase
from time import time

import jsonpickle
from nose.tools import assert_equal

from ..folder import summary_json

from .base_test import setup_tmp_dir, touch, assert_fixes
assert_fixes()

class FolderSummaryTest(TestCase):
    ''' Unittest class for folder summary json '''
    def setUp(self):
        ''' Test setup method '''
        self.tmp_dir, self.source_dir, self.destination_dir = setup_tmp_dir()
        self.now = int(time())
        mock_time = (self.now, self.now)
        touch(os.path.join(self.source_dir, 'file_1.pdf'), mock_time)
        touch(os.path.join(self.source_dir, 'file_2.pdf'), mock_time)
        touch(os.path.join(self.source_dir, 'file_3.pdf'), mock_time)
        os.makedirs(os.path.join(self.source_dir, 'another_folder'))
        touch(os.path.join(self.source_dir, 'another_folder', 'another_file.mp4'), mock_time)

    def teardown(self):
        ''' Test teardown method '''
        os.removedirs(self.tmp_dir)

    def test_successful_folder_summary_generation(self):
        ''' Validate summary_json returns folder information '''
        json = summary_json(self.source_dir)
        assert_equal(json, jsonpickle.encode({
            'files': [
                self.file_summary_dict('file_1.pdf'),
                self.file_summary_dict('file_2.pdf'),
                self.file_summary_dict('file_3.pdf')
            ],
            'folders': [
                self.file_summary_dict('another_folder', 102)
            ]
        }))

    def file_summary_dict(self, name, size=0):
        ''' File summary representation '''
        return {
            'name': name,
            'updated_at': self.now,
            'created_at': self.now,
            'size': size,
            'last_access_time': self.now
        }
