#! /usr/bin/env python

# ============================================================================
# Configuration file containing parameters and booleans to run initial part of
# the BART project. Edit lines below with correct information.
#
# Order of execution:
# 1. reads a BART.cfg file
# 2. makes a directory structure
# 3. copy relevant files to the current date directory
# 4. STEP 1 executes makeP.py to make a pressure file
# 5. STEP 2 executes makeAbun.py to make an abundances file
# 6. STEP 3 executes InitialPT.py to allow user to choose initial PT profile
# 7. STEP 3 executes makeatm.py to make a pre-atm file for TEA
# 8. STEP 4 executes TEA and makes a final atm file for Transit
# ============================================================================

# 2014-07-25 Jasmina Blecic, jasmina@physics.ucf.edu   Original version

import ConfigParser
import os
import subprocess
from InitialPT import *

# =================== READ BART.cfg FILE =================== #

# name of the configuration file
cfg_name = 'BART.cfg'

# Check if config file exists
try:
    f = open(cfg_name)
except IOError:
    print "\nConfig file is missing. Place the config file in the working directory\n"

# open config file
config = ConfigParser.RawConfigParser({})
config.read(cfg_name)

# read BART.cfg parameters
# directories and files parameters
loc_BART    = config.get('BART', 'loc_BART')
loc_TEA     = config.get('BART', 'loc_TEA')
loc_dir     = config.get('BART', 'loc_dir')
tep_name    = config.get('BART', 'tep_name')

# STEP 1 pressure parameters
n_layers    = config.getint('BART', 'n_layers')
p_top       = config.getfloat('BART', 'p_top')
p_bottom    = config.getfloat('BART', 'p_bottom')
log         = config.getboolean('BART', 'log')
press_name  = config.get('BART', 'press_name')

# STEP 2 abundances file parameters
abun_basic  = config.get('BART', 'abun_basic')
solar_times = config.getfloat('BART', 'solar_times')
COswap      = config.getboolean('BART', 'COswap')
abun_name   = config.get('BART', 'abun_name')

# STEP 3 initial PT profile parameters
p3     = config.getfloat('BART', 'p3')
p1     = config.getfloat('BART', 'p1')
a2     = config.getfloat('BART', 'a2')
a1     = config.getfloat('BART', 'a1')
T3_fac = config.getfloat('BART', 'T3_fac')

# STEP 4 makeatm parameters
in_elem      = config.get('BART', 'in_elem')
out_spec     = config.get('BART', 'out_spec')
pre_atm_name = config.get('BART', 'pre_atm_name')

# STEP 5 run TEA parameters
output_dir = config.get('BART', 'output_dir')

# ========================================================== #

import sys
sys.path.append(loc_BART)
sys.path.append(loc_TEA)

import time
import os

import makeP as mP
import makeAbun as mA
from makeatm import *

import shutil


# ================ MAKE DIRECTORY STRUCTURE ================ #

# Make a subdirectory with the date and time
dirfmt = loc_dir + "%4d-%02d-%02d_%02d:%02d:%02d"
date_dir = dirfmt % time.localtime()[0:6]
os.mkdir(date_dir)


# ================= COPY FILES TO DATE DIR ================= #

# Copy configuration file to the date directory
shutil.copy2(cfg_name, date_dir)

# Check if tepfile exists
try:
    f = open(tep_name)
except IOError:
    print "\nTepfile is missing. Place the tepfile in the working directory\n"

# Copy tepfile to the date directory
shutil.copy2(tep_name, date_dir)


# ========================= STEP 1 ========================= #
# Make the pressure grid. Call makeP.py

# Give the full pressure file location
press_file = date_dir + "/" + press_name

# Call makeP.py
mP.makeP(n_layers, p_top, p_bottom, press_file, log)


# ========================= STEP 2 ========================= #
# Make the abundances file. Call makeAbun.py

# Basic abundances file (Asplund et al 2009)
abun_basic = loc_BART + 'abundances.txt'

# Give the full abundances file location
abun_file = date_dir + '/' + abun_name

# Call the makeAbun.py function
mA.makeAbun(abun_basic, abun_file, solar_times, COswap)


# ========================= STEP 3 ========================= #
# Choose initial PT profile
# Change the initial PT parameters in BART.cfg
#        until you reach the desired shape

# Get the full tepfile location
tepfile = date_dir + "/" + tep_name

# Plot initial PT
plot_initialPT(date_dir, tepfile, press_file, a1, a2, p1, p3, T3_fac)

# Wait for user to continue
raw_input('\nPress enter to continue, or quit and choose other initial PT parameters\n')


# ========================= STEP 4 ========================= #
# Make a pre-atm file for TEA. 

# Get the full pre-atm file location
pre_atm = date_dir + "/" + pre_atm_name

# Call makeatm.py
make_preatm(date_dir, tepfile, press_file, abun_file, in_elem, out_spec, pre_atm, a1, a2, p1, p3, T3_fac)


# ========================= STEP 5 ========================= #
# Make a final atm file for Transit. Inputs for TEA

# Locate TEA runatm.py module
loc_runatm = loc_TEA + "runatm.py"

# Locate TEA output atmospheric file
tea_output = loc_TEA + "results/" + output_dir + "/" + output_dir + ".tea"

# Run TEA
proc=subprocess.Popen([loc_runatm, pre_atm, output_dir], cwd=loc_TEA)
proc.communicate()

# Copy the TEA result file 
shutil.copy2(tea_output, date_dir)


