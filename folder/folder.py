''' Folder Operations Public Interface '''
from stat import S_ISDIR, S_ISREG
import os
import jsonpickle

def summary_json(path):
    ''' Initialize a folder with metadata used by sync_folders '''
    folders, files = [], []
    for entry in os.listdir(path):
        stat = os.stat(os.path.join(path, entry))
        if S_ISDIR(stat.st_mode):
            folders.append(entry_dict(entry, stat))
        elif S_ISREG(stat.st_mode):
            files.append(entry_dict(entry, stat))
    return jsonpickle.encode({'files': files, 'folders': folders})

def entry_dict(entry_name, stat):
    ''' File summary entry dict representation '''
    return {
        'name': entry_name,
        'size': stat.st_size,
        'created_at': int(stat.st_ctime),
        'updated_at': int(stat.st_mtime),
        'last_access_time': int(stat.st_atime),
    }
