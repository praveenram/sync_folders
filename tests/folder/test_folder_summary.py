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

        self.summary = {
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
        }

    def teardown_method(self, method):
        shutil.rmtree(self.tmp_dir)

    def test_successful_folder_summary_generation(self, mocker):
        mocker.patch.object(Stat, 'timestamps', [1, 2, 3])
        mocker.patch.object(Stat, 'size', 1024)

        [json_string, children] = folder.summary_json(self.source_dir)

        assert json_string == jsonpickle.encode(self.summary)

        assert children == [os.path.join(self.source_dir, 'another_folder')]

    def test_ignore_init_file_during_folder_summary_generation(self, mocker):
        mocker.patch.object(Stat, 'timestamps', [1, 2, 3])
        mocker.patch.object(Stat, 'size', 1024)
        touch(os.path.join(self.source_dir, '.sync_folders.init'))

        [json_string, children] = folder.summary_json(self.source_dir)

        assert json_string.find('.sync_folders.init') == -1

    def test_empty_folder_summary_for_empty_folder(self):
        shutil.rmtree(self.source_dir)
        os.makedirs(self.source_dir)

        [json_string, children] = folder.summary_json(self.source_dir)

        assert json_string == jsonpickle.encode({
            'path': self.source_dir,
            'file_names': [],
            'folder_names': [],
            'files': {},
            'folders': {}
        })

        assert children == []

    def test_get_summary_for_folder_if_summary_present(self):
        open(os.path.join(self.source_dir, '.sync_folders.init'), 'w').write(
            jsonpickle.encode(self.summary)
        )

        assert folder.get_summary(self.source_dir) == self.summary

    def test_get_summary_generates_folder_summary_if_summary_not_present(self, mocker):
        mocker.patch.object(Stat, 'timestamps', [1, 2, 3])
        mocker.patch.object(Stat, 'size', 1024)

        assert folder.get_summary(self.source_dir) == self.summary

    def file_summary_dict(self, name):
        ''' File summary representation '''
        return {
            'name': name,
            'updated_at': 2,
            'created_at': 1,
            'size': 1024,
            'last_access_time': 3
        }
