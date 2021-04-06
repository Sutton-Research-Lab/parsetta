#! /usr/bin/env python
# -*- coding: utf-8 -*-

from . import utils as u
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
        
    def retrieve(self, prop, mat='all', struct=None, polymorph_info=False, chem_info=False, cond=None, ret=True, keep=False):
        """ Retrieve material information by quantitative ranking of property.
        
        **Parameters**\n
        prop: str
            Name of the property to retrieve.
        mat: str/list | 'all'
            List of materials compositions (in formula). Input 'all' indicates all materials.
        struct: str | None
            Type of structure to retrieve ('dft_structure', 'spuds_structure', etc), ``None`` for no structure.
        polymorph_info: bool | False
            Option to include all polymorph-dependent information (structures and properties) available for selected material.
        chem_info: bool | False
            Option to include the chemical information for the selected material (same for all polymorphs).
        cond: str/int | None
            Condition to filter the data according to property ('max', 'min', or an non-negative integer as the ranking).
        ret: bool | True
            Option to return the retrieved structures directly.
        keep: bool | False
            Option to keep the retrieved structure as an attribute of the instantiated class.
        """
        
        if mat == 'all':
            matforms = self.matforms
        else:
            matforms = mat
        
        retdict = {}
        for mf in matforms:
            
            # Retrieve chemical information
            chemdict = self.matdict[mf].copy()
            chemdict.pop('results')

            res_str = '{}.results'.format(mf)
            # Retrieve all tilts for a material (dictionary keys are '#_tilt', with # being an integer)
            tiltdict = glom(self.matdict, res_str)
            tiltnames = list(tiltdict.keys())
            propvals = nl.nested_lookup(prop, self.matdict[mf])
            
            if cond is not None:
                
                # Select the structures according to property ranking
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
                
                # Aggregate outcome after property ranking
                # Outcome with all information (and related structures)
                if polymorph_info:
                    propdict = {'tilt':tiltnames[idx]}
                    propdict.update(tiltdict[tiltnames[idx]])
                # Outcome with only single structure and corresponding property information
                elif struct is not None:
                    propdict = {'tilt':tiltnames[idx], prop: propvals[idx]}
                    struct_str = '{}.{}'.format(tiltnames[idx], struct)
                    struct_selected = glom(tiltdict, struct_str)
                    propdict = {'tilt':tiltnames[idx], prop: propvals[idx], struct: struct_selected}
                # Outcome with only property information
                else:
                    propdict = {'tilt':tiltnames[idx], prop: propvals[idx]}
            
            else:
                propdict = dict(zip(tiltnames, propvals))

            if chem_info:
                propdict.update(chemdict)
            
            retdict[mf] = propdict
            
        if ret:
            return retdict
        if keep:
            self.retdict = retdict

    def display(self, content):
        """ Display file structure in pretty print.
        """

        pprint(content)


class MatFilter(object):
    """ Filter out duplicate materials by specific properties.
    """
    
    def __init__(self, matdata):
        
        self.materials = MatParser(matdata)
    
    def select_reference(self, prop='FE_at', cond='max', struct='dft_structure', **kwargs):
        """ Select reference structures.
        """
        
        self.prop = prop
        self.struct = struct
        self.matref = self.materials.retrieve(prop, cond=cond, struct=struct, **kwargs)
    
    def filter_duplicate(self, prop='FE_at', conds=[2], rtol=1e-2, **kwargs):
        """ Filter duplicate structures.
        """
        
        self.other_materials = kwargs.pop('other_materials', [])
        
        struct = kwargs.pop('struct', self.struct)
        for cd in conds:
            othermats = {}
            others = self.materials.retrieve(prop, cond=cd, struct=struct)
        
            for (otherform, otherinfo), (refform, refinfo) in zip(self.matref.items(), others.items()):
                if not np.allclose(otherinfo[prop], refinfo[prop], rtol=rtol):
                    othermats[otherform] = otherinfo
        
            self.other_materials.append(othermats)
    
    def export(self, fdir='./', fstr='', **kwargs):
        """ Save (filtered) data. 
        """
        
        filtered_data = kwargs.pop('data', self.other_materials)
        indent = kwargs.pop('indent', 4)
        if len(filtered_data) == 1:
            for om in filtered_data:
                u.write_json(om, fdir + fstr + r'.json', indent=indent, **kwargs)
        else:
            for iom, om in enumerate(filtered_data):
                u.write_json(om, fdir + fstr + r'_{}.json'.format(str(iom).zfill(2)), indent=indent, **kwargs)