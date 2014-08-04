#! /usr/bin/env python

import numpy as np
import os

def makeAbun(abun_basic, filename, solar_times=1, COswap=False): 
    '''
    Function to make the abundaces file to be used by BART.
    The function uses Asplund et al (2009) elemental abundances file
    (abudances.txt) and multiplies the abundances by the number user wants,
    or swaps the C/O ratio. It is called by BART_config.py. 
  
    Parameters:
    -----------
    input_dir:  string
                Name of the inputs directory
    abun_basic: string
                Name of the basic abundances file (default:abundances.txt)
    filename:   string
                Name of the file.

    Optional parameters:
    --------------------
    solar_times=1: integer
              Defines multiplication factor of Asplund et al (2009)
              elemental abundances
    COswap=False: boolean
              If 'True' it will swap the abundances of C and O

    Returns:
    --------
    None

    Revisions
    ---------
    2014-07-12 0.1  Jasmina Blecic, jasmina@physics.ucf.edu   Original version
    '''

    # Put abundances file into inputs directory, create if non-existent
    #abun_dir = "inputs/abundances/"
    #if not os.path.exists(abun_dir): os.makedirs(abun_dir)  

    # Read the basic Aplsund ate al (2009) solar abundances file - abundances.txt 
    f = open(abun_basic, 'r')
    abundata = []
    for line in f.readlines():
        if line.startswith('#'):
            continue
        else:
            l = [value for value in line.split()]
            abundata.append(l)
    abundata = np.asarray(abundata)
    f.close()

    # Make a copy of abundata
    abundata_copy = np.copy(abundata)

    # Size of the abundata
    abun_size = len(abundata)

    # If user wants solar abundances adundata are not changed
    if solar_times == 1 and COswap == False:
        abundata = abundata
 
    # If user wants some multiplication of solar abundances
    elif solar_times != 1  and COswap == False:
        for i in np.arange(abun_size):
            # Multiple metal counts with the number user wants
            abundata[i][2] = float(abundata[i][2]) + np.log10(solar_times)
            abundata[i][2] = '%2.2f'%(np.float(abundata[i][2]))
        # Preserve H and He count as it was before
        abundata[1][2] = abundata_copy[1][2] 
        abundata[2][2] = abundata_copy[2][2]

    # If solar but COswap=True, swap the C/O ratio
    elif solar_times == 1 and COswap == True:
        # Take the original values from the copy of 'abundances.txt' file
        abundata[6][2] = abundata_copy[8][2]
        abundata[8][2] = abundata_copy[6][2]

    # If NONsolar but COswap=True, swap the C/O ratio and multiply abundances
    elif solar_times != 1 and COswap == True:
        # Take the original values from the copy of 'abundances.txt' file
        abundata[6][2] = abundata_copy[8][2]
        abundata[8][2] = abundata_copy[6][2]
        for i in np.arange(abun_size):
            # Multiple metal counts with the number user wants
            abundata[i][2] = float(abundata[i][2]) + np.log10(solar_times)
            # Constrain the decimal spaces to 2
            abundata[i][2] = '%2.2f'%(np.float(abundata[i][2]))
        # Preserve H and He count as it was before
        abundata[1][2] = abundata_copy[1][2] 
        abundata[2][2] = abundata_copy[2][2]

    # Place abundance file into inputs directory 
    abun_out = filename

    # Open new abudances file to write 
    f = open(str(abun_out), 'w+')

    # Write header
    header= "# This file contains solar abundances as found by Asplund et al. 2009. \n\
# The file is in the public domain. Contact: jasmina@physics.ucf.edu \n\
# Columns: ordinal, symbol, dex abundances, name, molar mass. \n"
    f.write(header)

    # Write data
    for i in np.arange(abun_size):
        # Write abundata in raws
        f.write(abundata[i][0].ljust(3) + ' ' + abundata[i][1].ljust(3) + ' ' + \
        abundata[i][2].ljust(5) + ' ' + abundata[i][3].ljust(13) + ' '  + \
        abundata[i][4].ljust(15) + '\n')
    f.close()


