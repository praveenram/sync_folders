''' Compare two folders and generate the diff of file tranfers required '''
import os

from folder import get_summary

class FolderCompare(object):
    ''' Methods to compare folders '''
    def __init__(self, source, destination):
        self.source_dir = source
        self.destination_dir = destination

        self.source_json = get_summary(source)
        self.destination_json = get_summary(destination)

    def compute_diff(self):
        diff = {}
        diff['copy'] = [self._to_from_to_dict(x) for x in self.files_to_copy()]
        return diff

    def files_to_copy(self):
        return list(
            set(self.source_json['file_names']).difference(self.destination_json['file_names'])
            )

    def _to_from_to_dict(self, name):
        from_path = self.source_json['path']
        to_path = self.destination_json['path']

        return {
            'from': os.path.join(from_path, name),
            'to': os.path.join(to_path, name)
        }
