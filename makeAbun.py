#! /usr/bin/env python

import numpy as np
import os
from BARTconfig import *

def makeAbun(filename, solar_times=1, swap=False): 
    '''
    Function to make the abundaces file to be used by BART.
    The function uses Asplund et al (2009) elemental abundances file
    abudances.txt and multiplies the abundances by the number user wants,
    or swaps the C/O ratio.
  
    Parameters:
    -----------
    filename: string
              Name of the file.

    Optional parameters:
    --------------------
    solar_times=1: integer
              Defines multiplication factor of Asplund et al (2009)
              elemental abundances
    swap=False: boolean
              If 'True' it will swap the abundances of C and O

    Returns:
    --------
    None

    Revisions
    ---------
    2014-06-28 0.1  Jasmina Blecic, jasmina@physics.ucf.edu   Original version
    '''

    # Put abundances file into inputs directory, create if non-existent
    abun_dir = "inputs/abundances/"
    if not os.path.exists(abun_dir): os.makedirs(abun_dir)  

    # Read the basic Aplsund ate al (2009) solar abundances file - abundances.txt 
    f = open(abun_file, 'r')
    abundata = []
    for line in f.readlines():
        l = [value for value in line.split()]
        abundata.append(l)
    abundata = np.asarray(abundata)
    f.close()

    # Make a copy of abundata
    abundata_copy = np.copy(abundata)

    # Size of the abundata
    abun_size = len(abundata)

    # If user wants solar abundances adundata are not changed
    if solar_times == 1 and swap == False:
        abundata = abundata
 
    # If user wants some multiplication of solar abundances
    elif solar_times != 1  and swap == False:
        for i in np.arange(abun_size):
            # Multiple metal counts with the number user wants
            abundata[i][2] = float(abundata[i][2]) + np.log10(solar_times)
            abundata[i][2] = '%2.2f'%(np.float(abundata[i][2]))
        # Preserve H and He count as it was before
        abundata[1][2] = abundata_copy[1][2] 
        abundata[2][2] = abundata_copy[2][2]

    # If solar but swap=True, swap the C/O ratio
    elif solar_times == 1 and swap == True:
        # Take the original values from the copy of 'abundances.txt' file
        abundata[6][2] = abundata_copy[8][2]
        abundata[8][2] = abundata_copy[6][2]

    # If NONsolar but swap=True, swap the C/O ratio and multiply abundances
    elif solar_times != 1 and swap == True:
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
    abun_out = abun_dir + filename

    # Open new abudances file to write 
    f = open(str(abun_out), 'w+')

    for i in np.arange(abun_size):
        # Write abundata in raws
        f.write(abundata[i][0].ljust(4) + ' ' + abundata[i][1].ljust(4) + ' ' + \
        abundata[i][2].ljust(6) + ' ' + abundata[i][3].ljust(12) + ' '  + \
        abundata[i][4].ljust(15) + '\n')
    f.close()

# Call the function to execute
if __name__ == '__main__':
   
    # Set parameters
    solar_times = 5
    swap = True

    # Set filename
    filename = 'abun5solar-NoSwap.txt'  

    # Call the function
    makeAbun(filename, solar_times, swap)

