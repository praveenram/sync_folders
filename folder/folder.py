''' Folder Operations Public Interface '''
import os
import jsonpickle

from ._os import is_directory, is_file, Stat

def init_folder(path):
    ''' Initialize a folder with a metadata file used by sync_folders '''
    folders = [path]
    while folders:
        current_path = folders.pop(0)
        [summary, children] = summary_json(current_path)
        open(os.path.join(current_path, '.sync_folders.init'), 'w').write(summary)
        folders.extend(children)

def summary_json(path):
    ''' Generates folder summary for metadata file '''
    folders, files, child_folders = [], [], []
    for entry in os.listdir(path):
        stat = Stat(os.path.join(path, entry))
        if is_directory(stat):
            child_folders.append(os.path.join(path, entry))
            folders.append(entry_dict(entry, stat))
        elif is_file(stat):
            files.append(entry_dict(entry, stat))

    folders = sorted(folders, key=lambda entry: entry['name'])
    files = sorted(files, key=lambda entry: entry['name'])

    return [jsonpickle.encode({'files': files, 'folders': folders}), child_folders]

def entry_dict(entry_name, stat):
    ''' File/Folder summary entry dict representation '''
    timestamps = stat.timestamps
    return {
        'name': entry_name,
        'size': stat.size,
        'created_at': int(timestamps[0]),
        'updated_at': int(timestamps[1]),
        'last_access_time': int(timestamps[2]),
    }
