## Synchronize Contents of Folder A with Folder B (not rsync)

Command line tool to intelligently backup a folder (make an exact duplicate) into a new path.

Copies only the diff, goal is to have something faster than `rsync` for large number of files.

Usage:

`sync_folders /tmp/folder_1 /tmp/folder_2`
