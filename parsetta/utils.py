#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import json


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