
# ===================================================================
# Configuration file containing parameters and booleans to run BART.
# Edit lines below with correct information.
#
# Correct order of execution:
# 1. run makeP.py to make a pressure file
# 2. run makeAbun.py to make an abundances file
# 3. run makeatm.py to make a pre-atm file
# 4. run TEA to make an atm file
# ===================================================================

# 2014-07-01 Jasmina Blecic, jasmina@physics.ucf.edu   Version 1.0

# Location and the name of the tepfile
tepfile       = 'inputs/tepfile/HD209458b.tep'

# Location and the name of the pressure file
press_file = 'inputs/press_file/Rojo-test.txt'

# Location and the name of the elemental abundance file
abun_file    = 'inputs/abundances/abundances.txt'

# Location and the name of the filter file
filter_file_loc   = 'inputs/'

# Location and the name of the transit config file
transit_conf_loc  = 'inputs/Eclipse-test.cfg'

# Location and the name of the (MC)^3 file
MC3_file_loc      = 'inputs/MC3_file/MC3_config.cfg'

# Location of the data
data_loc = 'inputs/'

# Name of the pre-atm file to be made by makeatm.py
pre_atm = 'Rojo-test.dat'

# Location and name of the final atm file
atm_file = 'TEA/results/Rojo/Rojo.dat'

# Elemental species of interest used by makeatm.py
in_elem  = "C H He O N"

# Output specise of interest
#                   MUST use names produced by JANAF.py
#                   MUST include all elemental species
#                   see TEA/converstion-record-sort.txt for the correct names
out_spec = "H_g He_ref C_g N_g O_g H2_ref CO_g CO2_g CH4_g H2O_g NH3_g C2H2_g C2H4_g"

