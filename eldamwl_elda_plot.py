import numpy as np
from eldamwl import Eldamwl, set_profile_color
from elda import Elda
import glob
import matplotlib.pyplot as plt
import argparse
from plotting import make_plots

parser=argparse.ArgumentParser(description="Plot SCC Optical Products")
parser.add_argument("-i", "--eldamwl", required=True, help="Path to the ELDAmwl file to plot")
parser.add_argument("-e", "--elda", required=True, help="Path to the directory containing ELDA files to plot")
args=parser.parse_args()

# Open ELDAmwl file
ew = Eldamwl()
ew.from_netcdf(args.eldamwl)
#ew.plot()

# Open ELDA files
ee=[]
elda_pattern=args.elda+"/*.nc"
for ff in glob.glob(elda_pattern):
    buffer=Elda()
    buffer.from_netcdf(ff)
    ee.append(buffer)

# Generate plot
make_plots(ew, ee)
