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
        ''' Recursively find the files / folders to copy and delete b/w source and destination '''
        files_to_copy = self.new_files() + self.modified_files()
        new_folders = self.new_folders()
        existing_folders = self.source_json['folder_names_set'].difference(new_folders)

        diff = {'copy': [], 'copy_folders': [], 'delete': [], 'delete_folders': []}

        for folder in existing_folders:
            subfolder = FolderCompare(
                os.path.join(self.source_dir, folder),
                os.path.join(self.destination_dir, folder)
            )
            subfolder_diff = subfolder.compute_diff()
            diff['copy'].extend(subfolder_diff['copy'])
            diff['copy_folders'].extend(subfolder_diff['copy_folders'])
            diff['delete'].extend(subfolder_diff['delete'])
            diff['delete_folders'].extend(subfolder_diff['delete_folders'])

        diff['copy'].extend([self._to_from_to_dict(x) for x in files_to_copy])
        diff['copy_folders'].extend([self._to_from_to_dict(x) for x in new_folders])
        diff['delete'].extend([self._to_destination_path(x) for x in self.files_to_delete()])
        diff['delete_folders'].extend(
            [self._to_destination_path(x) for x in self.folders_to_delete()]
        )

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

    def files_to_delete(self):
        return list(
            self.destination_json['file_names_set'].difference(
                self.source_json['file_names_set']
            )
        )

    def folders_to_delete(self):
        return list(
            self.destination_json['folder_names_set'].difference(
                self.source_json['folder_names_set']
            )
        )

    def modified_files(self):
        _modified_files = []
        common_files = self.source_json['file_names_set'].intersection(
            self.destination_json['file_names_set']
        )
        for file in common_files:
            if self.source_json['files'][file] != self.destination_json['files'][file]:
                _modified_files.append(file)

        return _modified_files

    def _to_from_to_dict(self, name):
        from_path = self.source_json['path']
        to_path = self.destination_json['path']

        return {
            'from': os.path.join(from_path, name),
            'to': os.path.join(to_path, name)
        }

    def _to_destination_path(self, name):
        return os.path.join(self.destination_json['path'], name)
