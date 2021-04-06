#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import json
import cloudpickle as cpk
import glob as g
import natsort as nts


def read_json(file, **kwds):
    """ Read json file.
    """

    with open(file) as f:
        return json.load(f, **kwds)


def write_json(dic, file, **kwds):
    """ Write a dictionary into json.
    """

    with open(file, 'w') as f:
        json.dump(dic, f, **kwds)


def pickle_file(obj, file):
    """ Pickle object to file.
    """

    with open(file, 'wb') as f:
        cpk.dump(obj, f)


def load_pickle(file):
    """ Load pickled file.
    """

    with open(file, 'rb') as f:
        return cpk.load(f)


def findFiles(fdir, fstring='', ftype='h5', **kwds):
    """
    Retrieve files named in a similar way from a folder.
    
    :Parameters:
        fdir : str
            Folder name where the files are stored.
        fstring : str | ''
            Extra string in the filename.
        ftype : str | 'h5'
            The type of files to retrieve.
        **kwds : keyword arguments
            Extra keywords for `natsorted()`.
    """
    
    files = nts.natsorted(g.glob(fdir + fstring + '.' + ftype), **kwds)
    
    return files