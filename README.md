# Overview

This package provides utilities to handle NetCDF file produced by ELDA or ELDAmwl. ELDA (EARLINET Lidar Data Analizer) and ELDAmwl (EARLINET Lidar Data Analizer Multiwavelength) are modules of EARLINET's Single Calculus Chain focused on the calculation of vertical profiles of atmospheric aerosol optical properties.


## Installation
To be completed.

## How to compare ELDAmwl and ELDA products 

The package includes a Python script `eldamwl_elda_plot.py` that should be called as:

`python eldamwl_elda_plot.py [command line arguments]`

The usage of the script program is described below:

```
usage: eldamwl_elda_plot.py [-h] -i ELDAMWL -e ELDA

Plot SCC Optical Products

options:
  -h, --help            show this help message and exit
  -i ELDAMWL, --eldamwl ELDAMWL
                        Path to the ELDAmwl file to plot
  -e ELDA, --elda ELDA  Path to the directory containing ELDA files to plot
```  

## Usage in python code

The package provides two main classes `ELDAmwl` and `ELDA` reflecting the data structure of NetCDF file produced by the two SCC modules.

A typical usage is described below:

```python
import glob  # This is needed to read a list of filenames
from eldamwl import Eldamwl
from elda import Elda

# Go to the directory where ELDAmwl files are stored
cd /path/to/lidar/files

# Read the ELDAmwl filenames
eldamwl_filenames = glob.glob("*.nc") # The *.nc reads all the files in the current directory.

# Read the ELDAmwl files
eldamwl=[]
for ff in eldamwl_filenames:
    buffer=Eldamwl()
    buffer.from_netcdf(ff)
    eldamwl.append(buffer)

# Go to the directory where ELDA files are stored
cd /path/to/lidar/files

# Read the ELDA filenames
elda_filenames = glob.glob("*.nc") # The *.nc reads all the files in the current directory.

# Read the ELDA files
elda=[]
for ff in elda_filenames:
    buffer=Elda()
    buffer.from_netcdf(ff)
    elda.append(buffer)

# Plotting examples
elda[0].plot()
elamwl[1].plot()
```  
