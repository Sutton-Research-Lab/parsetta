#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import json


def read_json(json):
    """ Read json file.
    """

    with open(json) as f:
        return json.load(f)