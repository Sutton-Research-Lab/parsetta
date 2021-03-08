#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from glom import glom
import nested_lookup as nl
try:
    from pprint import pprint
except:
    pass


class MatParser(object):
    """ Parser class for ``pymatgen`` materials data structure.
    """
    
    def __init__(self, matdict):
        
        self.matdict = matdict
        self.matforms = list(matdict.keys())
        
    @property
    def nmat(self):
        
        return len(self.matforms)
        
    def retrieve(self, prop, mat='all', struct=None, cond=None, ret=True, keep=False):
        """ Retrieve material structure by property.
        
        **Parameters**\n
        prop: str
            Name of the property to retrieve.
        mat: str/list | 'all'
            List of materials compositions (in formula). Input 'all' indicates all materials.
        struct: str | None
            Type of structure to retrieve ('dft_structure', 'spuds_structure', etc), ``None`` for no structure.
        cond: str/int | None
            Condition to filter the data according to property ('max', 'min', or an non-negative integer as the ranking).
        ret: bool | True
            Option to return the retrieved structures directly.
        keep: bool | False
            Option to keep the retrieved structure as an attribute.
        """
        
        if mat == 'all':
            matforms = self.matforms
        else:
            matforms = mat
        
        retdict = {}
        for mf in matforms:
            
            res_str = '{}.results'.format(mf)
            tiltdict = glom(self.matdict, res_str)
            tiltnames = list(tiltdict.keys())
            propvals = nl.nested_lookup(prop, self.matdict[mf])
            
            if cond is not None:
                # Retrieve the structure with the lowest property value
                if cond == 'min':
                    idx = np.argmin(propvals)
                # Retrieve the structure with the highest property value
                elif cond == 'max':
                    idx = np.argmax(propvals)
                # Retrieve the structure with the property value ranked at the place cond
                elif isinstance(cond, int):
                    idx = np.argsort(propvals)[cond]
                else:
                    raise NotImplementedError
                
                if struct is not None:
                    struct_str = '{}.{}'.format(tiltnames[idx], struct)
                    struct_selected = glom(tiltdict, struct_str)
                    propdict = {'tilt':tiltnames[idx], prop: propvals[idx], struct: struct_selected}
                else:
                    propdict = {'tilt':tiltnames[idx], prop: propvals[idx]}    
            
            else:
                propdict = dict(zip(tiltnames, propvals))
            
            retdict[mf] = propdict
            
        if ret:
            return retdict
        if keep:
            self.retdict = retdict

    def display(self, content):
        """ Display file structure in pretty print.
        """

        pprint(content)