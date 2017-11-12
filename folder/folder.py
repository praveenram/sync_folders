''' Folder Operations Public Interface '''
import os
import jsonpickle
from ._os import is_directory, is_file, Stat

def summary_json(path):
    ''' Initialize a folder with metadata used by sync_folders '''
    folders, files = [], []
    for entry in os.listdir(path):
        stat = Stat(os.path.join(path, entry))
        if is_directory(stat):
            folders.append(entry_dict(entry, stat))
        elif is_file(stat):
            files.append(entry_dict(entry, stat))

    folders = sorted(folders, key=lambda entry: entry['name'])
    files = sorted(files, key=lambda entry: entry['name'])

    return jsonpickle.encode({'files': files, 'folders': folders})

def entry_dict(entry_name, stat):
    ''' File summary entry dict representation '''
    timestamps = stat.timestamps
    return {
        'name': entry_name,
        'size': stat.size,
        'created_at': int(timestamps[0]),
        'updated_at': int(timestamps[1]),
        'last_access_time': int(timestamps[2]),
    }
