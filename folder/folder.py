''' Folder Operations Public Interface '''
import os
import jsonpickle

def init(path):
    ''' Initialize a folder with metadata used by sync_folders '''
    folders, files = [], []
    for entry in os.listdir(path):
        if os.path.isdir(entry):
            folders.append(entry)
        else:
            files.append(entry)
    return jsonpickle.encode({'files': files, 'folders': folders})
