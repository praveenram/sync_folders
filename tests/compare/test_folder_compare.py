''' Unit tests for compare folder_compare '''
import os
import shutil
import pytest
from pytest_mock import mocker

import jsonpickle

import compare
from compare.folder_compare import FolderCompare

class TestFolderCompare(object):
    def setup_method(self, method):
        self.source_folder_json = {
            'path': '/tmp/source/path',
            'file_names': ['file_1.pdf', 'file_2.pdf', 'file_3.pdf'],
            'folder_names': ['another_folder'],
            'files': {
                'file_1.pdf': self._file_summary_dict('file_1.pdf'),
                'file_2.pdf': self._file_summary_dict('file_2.pdf'),
                'file_3.pdf': self._file_summary_dict('file_3.pdf')
            },
            'folders': {
                'another_folder': self._file_summary_dict('another_folder')
            }
        }
        os.makedirs('/tmp/source/path')
        open('/tmp/source/path/.sync_folders.init', 'w').write(jsonpickle.encode(self.source_folder_json))

        self.destination_folder_json = {
            'path': '/tmp/destination/path',
            'file_names': [],
            'folder_names': [],
            'files': {},
            'folders': {}
        }
        os.makedirs('/tmp/destination/path')
        open('/tmp/destination/path/.sync_folders.init', 'w').write(jsonpickle.encode(self.destination_folder_json))

    def teardown_method(self, method):
        shutil.rmtree('/tmp/source')
        shutil.rmtree('/tmp/destination')


    def test_copy_if_destination_does_not_have_file(self):
        compare = FolderCompare('/tmp/source/path', '/tmp/destination/path')

        diff = compare.compute_diff()

        assert { 'from': '/tmp/source/path/file_1.pdf', 'to': '/tmp/destination/path/file_1.pdf'} in diff['copy']
        assert { 'from': '/tmp/source/path/file_2.pdf', 'to': '/tmp/destination/path/file_2.pdf'}  in diff['copy']
        assert { 'from': '/tmp/source/path/file_3.pdf', 'to': '/tmp/destination/path/file_3.pdf'}  in diff['copy']

    def test_copy_folder_if_destination_does_not_have_folder(self):
        compare = FolderCompare('/tmp/source/path', '/tmp/destination/path')

        diff = compare.compute_diff()

        assert { 'from': '/tmp/source/path/another_folder', 'to': '/tmp/destination/path/another_folder'} in diff['copy']

    def _file_summary_dict(self, name):
        ''' File summary representation '''
        return {
            'name': name,
            'updated_at': 2,
            'created_at': 1,
            'size': 1024,
            'last_access_time': 3
        }
