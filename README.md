## Synchronize Contents of Folder A with Folder B (not rsync)

[![Build Status](https://travis-ci.org/praveenram/sync_folders.svg?branch=master)](https://travis-ci.org/praveenram/sync_folders)

[![Code Climate](https://codeclimate.com/github/praveenram/sync_folders/badges/gpa.svg)](https://codeclimate.com/github/praveenram/sync_folders)

[![Issue Count](https://codeclimate.com/github/praveenram/sync_folders/badges/issue_count.svg)](https://codeclimate.com/github/praveenram/sync_folders)

Command line tool to intelligently backup a folder (make an exact duplicate) into a new path.

Copies only the diff, goal is to have something faster than `rsync` for large number of files.

Usage:

`sync_folders /tmp/folder_1 /tmp/folder_2`
