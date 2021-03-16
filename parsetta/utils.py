#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import json
import cloudpickle as cpk


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