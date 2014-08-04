#! /usr/bin/env python

import numpy as np
import os


def makeP(n_layers, p_top, p_bottom, filename, log=True): 
    '''
    Function to make the pressure array file to be used by BART.
    It is called by BART_config.py.
  
    Parameters:
    -----------
    n_layers: integer
              Number of layers in the atmosphere.
    p_top: float
              Pressure at the top of the atmosphere.
    p_bottom:
              Pressure at the bottom of the atmopshere.
    filename: string
              Name of the file to be produced.
    log: boolean
             If True, logarithmic sampling of the pressure range is choosen,
             else linear.

    Returns:
    --------
    None

    Revisions
    ---------
    2014-06-22 0.1  Jasmina Blecic, jasmina@physics.ucf.edu   Original version
    '''

    # Put abundances file into inputs directory, create if non-existent
    #pres_dir = "inputs/press_file/"
    #if not os.path.exists(pres_dir): os.makedirs(pres_dir)    

    # If log=True the logarithmic sampling is chosen, else linear
    if log:
        pres = np.logspace( np.log10(np.float(p_top)), np.log10(np.float(p_bottom)), n_layers)   
    else:
        pres = np.linspace( p_top, p_bottom, n_layers)   

    # Write header line
    header      = "Layer  P [bar] \n"

    # Place pressure file into inputs directory 
    #pres_out = pres_dir + filename

    # Open file to write 
    f = open(str(filename), 'w+')
    f.write(header)

    for i in np.arange(n_layers):
        # Layer number
        f.write(str(i+1).ljust(6) + ' ')

        # Pressure list
        f.write(str('%4.4e'%pres[i]).ljust(10) + ' ' + '\n')
    f.close()

