''' Compare two folders and generate the diff of file tranfers required '''
import os

from folder import get_summary

def _initialize_sets(summary_dict):
    summary_dict['file_names_set'] = set(summary_dict['file_names'])
    summary_dict['folder_names_set'] = set(summary_dict['folder_names'])

class FolderCompare(object):
    ''' Methods to compare folders '''
    def __init__(self, source, destination):
        self.source_dir = source
        self.destination_dir = destination

        self.source_json = get_summary(source)
        self.destination_json = get_summary(destination)

        _initialize_sets(self.source_json)
        _initialize_sets(self.destination_json)

    def compute_diff(self):
        diff = {}
        new_files_folders = self.new_files() + self.new_folders()
        diff['copy'] = [self._to_from_to_dict(x) for x in new_files_folders]
        return diff

    def new_files(self):
        return list(
            self.source_json['file_names_set'].difference(
                self.destination_json['file_names_set']
            )
        )

    def new_folders(self):
        return list(
            self.source_json['folder_names_set'].difference(
                self.destination_json['folder_names_set']
            )
        )

    def _to_from_to_dict(self, name):
        from_path = self.source_json['path']
        to_path = self.destination_json['path']

        return {
            'from': os.path.join(from_path, name),
            'to': os.path.join(to_path, name)
        }
