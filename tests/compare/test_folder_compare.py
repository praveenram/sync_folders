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
            'folder_names': ['another_folder', 'folder_2'],
            'files': {
                'file_1.pdf': self._file_summary_dict('file_1.pdf'),
                'file_2.pdf': self._file_summary_dict('file_2.pdf'),
                'file_3.pdf': self._file_summary_dict('file_3.pdf')
            },
            'folders': {
                'another_folder': self._file_summary_dict('another_folder'),
                'folder_2': self._file_summary_dict('folder_2')
            }
        }
        self.another_folder_json = {
            'path': '/tmp/source/path/another_folder',
            'file_names': ['another_file.mp4'],
            'folder_names': [],
            'files': {
                'another_file.mp4': self._file_summary_dict('another_file.mp4')
            },
            'folders': {}
        }
        self.folder_2_json = {
            'path': '/tmp/source/path/folder_2',
            'file_names': ['file.docx'],
            'folder_names': [],
            'files': {
                'file.docx': self._file_summary_dict('file.docx')
            },
            'folders': {}
        }
        os.makedirs('/tmp/source/path/another_folder')
        os.makedirs('/tmp/source/path/folder_2')
        open('/tmp/source/path/.sync_folders.init', 'w').write(jsonpickle.encode(self.source_folder_json))
        open('/tmp/source/path/another_folder/.sync_folders.init', 'w').write(jsonpickle.encode(self.another_folder_json))
        open('/tmp/source/path/folder_2/.sync_folders.init', 'w').write(jsonpickle.encode(self.folder_2_json))

        self.destination_folder_json = {
            'path': '/tmp/destination/path',
            'file_names': ['not_in_src.pptx'],
            'folder_names': ['folder_2', 'folder_to_delete'],
            'files': {
                'not_in_src.pptx': self._file_summary_dict('not_in_src.pptx')
            },
            'folders': {
                'folder_2': self._file_summary_dict('folder_2'),
                'folder_to_delete': self._file_summary_dict('folder_to_delete')
            }
        }
        self.dest_folder_2_json = {
            'path': '/tmp/destination/path/folder_2',
            'file_names': ['not_in_src.mov'],
            'folder_names': [],
            'files': {
                'not_in_src.mov': self._file_summary_dict('not_in_src.mov')
            },
            'folders': {}
        }
        self.dest_folder_to_delete_json = {
            'path': '/tmp/destination/path/folder_to_delete',
            'file_names': ['some_file.txt'],
            'folder_names': [],
            'files': {
                'some_file.txt': self._file_summary_dict('some_file.txt')
            },
            'folders': {}
        }
        os.makedirs('/tmp/destination/path/folder_2')
        os.makedirs('/tmp/destination/path/folder_to_delete')
        open('/tmp/destination/path/.sync_folders.init', 'w').write(jsonpickle.encode(self.destination_folder_json))
        open('/tmp/destination/path/folder_2/.sync_folders.init', 'w').write(jsonpickle.encode(self.dest_folder_2_json))
        open('/tmp/destination/path/folder_to_delete/.sync_folders.init', 'w').write(jsonpickle.encode(self.dest_folder_to_delete_json))

    def teardown_method(self, method):
        shutil.rmtree('/tmp/source')
        shutil.rmtree('/tmp/destination')

    def test_copy_if_destination_does_not_have_file(self):
        compare = FolderCompare('/tmp/source/path', '/tmp/destination/path')

        diff = compare.compute_diff()

        assert {'from': '/tmp/source/path/file_1.pdf', 'to': '/tmp/destination/path/file_1.pdf'} in diff['copy']
        assert {'from': '/tmp/source/path/file_2.pdf', 'to': '/tmp/destination/path/file_2.pdf'}  in diff['copy']
        assert {'from': '/tmp/source/path/file_3.pdf', 'to': '/tmp/destination/path/file_3.pdf'}  in diff['copy']

    def test_copy_folder_if_destination_does_not_have_folder(self):
        compare = FolderCompare('/tmp/source/path', '/tmp/destination/path')

        diff = compare.compute_diff()

        assert {'from': '/tmp/source/path/another_folder', 'to': '/tmp/destination/path/another_folder'} in diff['copy_folders']

    def test_copy_file_in_a_sub_folder_in_source(self):
        compare = FolderCompare('/tmp/source/path', '/tmp/destination/path')

        diff = compare.compute_diff()

        assert {'from': '/tmp/source/path/folder_2/file.docx', 'to': '/tmp/destination/path/folder_2/file.docx'} in diff['copy']

    def test_copy_folder_should_not_include_files_in_folder_marked_for_copy(self):
        compare = FolderCompare('/tmp/source/path', '/tmp/destination/path')

        diff = compare.compute_diff()

        assert {'from': '/tmp/source/path/another_folder/another_file.mp4', 'to': '/tmp/destination/path/another_folder/another_file.mp4'} not in diff['copy']

    def test_delete_file_if_not_in_source(self):
        compare = FolderCompare('/tmp/source/path', '/tmp/destination/path')

        diff = compare.compute_diff()

        assert '/tmp/destination/path/not_in_src.pptx' in diff['delete']

    def test_delete_folder_should_not_include_delete_for_files_in_folder_marked_for_deletion(self):
        compare = FolderCompare('/tmp/source/path', '/tmp/destination/path')

        diff = compare.compute_diff()

        assert '/tmp/destination/path/folder_to_delete' in diff['delete_folders']

    def test_delete_file_in_a_subfolder_of_source(self):
        compare = FolderCompare('/tmp/source/path', '/tmp/destination/path')

        diff = compare.compute_diff()

        assert '/tmp/destination/path/folder_2/not_in_src.mov' in diff['delete']

    def _file_summary_dict(self, name):
        ''' File summary representation '''
        return {
            'name': name,
            'updated_at': 2,
            'created_at': 1,
            'size': 1024,
            'last_access_time': 3
        }
