#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from glom import glom
import nested_lookup as nl


class MatParser(object):
    """ Parser class for materials data
    """
    
    def __init__(self, matdict):
        
        self.matdict = matdict
        self.matforms = list(matdict.keys())
        
    @property
    def nmat(self):
        
        return len(self.matforms)
    
    def retrieve(self, prop, mat='all', cond=None):
        """ Retrieve material by property.
        
        **Parameters**\n
        prop: str
            Name of the property to retrieve.
        mat: str/list | 'all'
            List of materials compositions (in formula). Input 'all' indicates all materials.
        cond: str | None
            Condition to filter the data according to property ('max' or 'min').
        """
            
        
        if mat == 'all':
            matforms = self.matforms
        else:
            matforms = mat
        
        retdict = {}
        for mf in matforms:
            
            res_str = mf + '.results'
            tiltdict = glom(self.matdict, res_str)
            tiltnames = list(tiltdict.keys())
            propvals = nl.nested_lookup(prop, self.matdict[mf])
            
            if cond is not None:
                if cond == 'min':
                    idx = np.argmin(propvals)
                elif cond == 'max':
                    idx = np.argmax(propvals)
                propdict = {tiltnames[idx]: propvals[idx]}    
            else:
                propdict = dict(zip(tiltnames, propvals))
            
            retdict[mf] = propdict
            
        return retdict