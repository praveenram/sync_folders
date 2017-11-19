''' Folder Operations Public Interface '''
import os
from pathlib import Path
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
    folders, files = {}, {}
    folder_names, file_names = [], []
    child_folders = []
    for entry in os.listdir(path):
        if entry == '.sync_folders.init':
            continue
        stat = Stat(os.path.join(path, entry))
        if is_directory(stat):
            child_folders.append(os.path.join(path, entry))
            folder_names.append(entry)
            folders[entry] = entry_dict(entry, stat)
        elif is_file(stat):
            file_names.append(entry)
            files[entry] = entry_dict(entry, stat)

    summary = jsonpickle.encode({
        'path': path,
        'file_names': sorted(file_names),
        'folder_names': sorted(folder_names),
        'files': files,
        'folders': folders
    })

    return [summary, child_folders]

def get_summary(path):
    summary_file = Path(os.path.join(path, '.sync_folders.init'))
    if not summary_file.exists():
        print('Initializing folder %s' % path)
        init_folder(path)

    return jsonpickle.decode(''.join(open(str(summary_file), 'r').readlines()))

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
