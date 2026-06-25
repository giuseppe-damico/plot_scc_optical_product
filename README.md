# Overview

This package provides utilities to handle NetCDF file produced by ELDA or ELDAmwl. ELDA (EARLINET Lidar Data Analizer) and ELDAmwl (EARLINET Lidar Data Analizer Multiwavelength) are modules of EARLINET's Single Calculus Chain focused on the calculation of vertical profiles of atmospheric aerosol optical properties.


## Installation

### 1. Install uv

On Linux and Mac

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone the repository

```
git clone https://github.com/giuseppe-damico/plot_scc_optical_product.git
```

### 3. Install dependencies

The command above will create a directory called "plot_scc_optical_product" 

```
cd plot_scc_optical_product
uv sync
```

### 4. Test the installation 

```
uv run python eldamwl_elda_plot.py -i tests/eldamwl/20250904pot192m/pot_012_0000734_202509041923_202509042019_20250904pot192m_ELDAmwl_v0.2.0.nc -e tests/elda/20250904pot192e
```

You can also use:

```
uv run eldamwl_elda_plot -i tests/eldamwl/20250904pot192m/pot_012_0000734_202509041923_202509042019_20250904pot192m_ELDAmwl_v0.2.0.nc -e tests/elda/20250904pot192e
```

If you prefer to activate the venv manually:

```
source .venv/bin/activate
```
and then type:

```
python eldamwl_elda_plot.py -i tests/eldamwl/20250904pot192m/pot_012_0000734_202509041923_202509042019_20250904pot192m_ELDAmwl_v0.2.0.nc -e tests/elda/20250904pot192e
```

or simply:

```
eldamwl_elda_plot -i tests/eldamwl/20250904pot192m/pot_012_0000734_202509041923_202509042019_20250904pot192m_ELDAmwl_v0.2.0.nc -e tests/elda/20250904pot192e
```




## How to compare ELDAmwl and ELDA products 

The package includes a Python script `eldamwl_elda_plot.py` requiring the following arguments:

```
usage: eldamwl_elda_plot.py [-h] -i ELDAMWL -e ELDA [-o filename]

Plot SCC Optical Products

options:
  -h, --help            show this help message and exit
  -i ELDAMWL, --eldamwl ELDAMWL
                        Path to the ELDAmwl file to plot
  -e ELDA, --elda ELDA  Path to the directory containing ELDA files to plot
  -o <filename>, --filename <filename>  
                        Full path of the png filename to save the plot 
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
