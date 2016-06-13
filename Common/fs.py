"""
Filesystem Stuff.
"""

import os


def get_fs_usage(fs='/volume1'):
    """
    Get filesystem usage for a given mount point.

    http://stackoverflow.com/a/12327880
    https://docs.python.org/release/2.6.8/library/os.html#os.statvfs
    http://pubs.opengroup.org/onlinepubs/009695399/basedefs/sys/statvfs.h.html

    @param: fs     - Filesystem Mount Point            [String]
    @return: usage - Usage (free, total, used) (Bytes) [Dict of Floats]
    """
    statvfs = os.statvfs(fs)
    total = statvfs.f_bsize * statvfs.f_blocks
    free = statvfs.f_bsize * statvfs.f_bavail
    used = total - free
    return { 'free': free, 'total': total, 'used': used }
