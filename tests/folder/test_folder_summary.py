''' Unit tests for folder summary_json '''
import os
from time import time
import pytest
from pytest_mock import mocker
import shutil

import jsonpickle

import folder
from folder._os import Stat

from ..base_test import setup_tmp_dir, touch

class TestFolderSummary(object):
    def setup_method(self, method):
        self.tmp_dir, self.source_dir, self.destination_dir = setup_tmp_dir()
        touch(os.path.join(self.source_dir, 'file_1.pdf'))
        touch(os.path.join(self.source_dir, 'file_2.pdf'))
        touch(os.path.join(self.source_dir, 'file_3.pdf'))
        os.makedirs(os.path.join(self.source_dir, 'another_folder'))
        touch(os.path.join(self.source_dir, 'another_folder', 'another_file.mp4'))

    def teardown_method(self, method):
        shutil.rmtree(self.tmp_dir)

    def test_successful_folder_summary_generation(self, mocker):
        mocker.patch.object(Stat, 'timestamps', [1, 2, 3])
        mocker.patch.object(Stat, 'size', 1024)

        [json, children] = folder.summary_json(self.source_dir)

        assert json == jsonpickle.encode({
            'path': self.source_dir,
            'file_names': ['file_1.pdf', 'file_2.pdf', 'file_3.pdf'],
            'folder_names': ['another_folder'],
            'files': {
                'file_1.pdf': self.file_summary_dict('file_1.pdf'),
                'file_2.pdf': self.file_summary_dict('file_2.pdf'),
                'file_3.pdf': self.file_summary_dict('file_3.pdf')
            },
            'folders': {
                'another_folder': self.file_summary_dict('another_folder')
            }
        })

        assert children == [os.path.join(self.source_dir, 'another_folder')]

    def file_summary_dict(self, name):
        ''' File summary representation '''
        return {
            'name': name,
            'updated_at': 2,
            'created_at': 1,
            'size': 1024,
            'last_access_time': 3
        }
