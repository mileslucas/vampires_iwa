# 2023/11/17 VAMPIRES IWA Measurement

**Author:** Miles Lucas <mdlucas@hawaii.edu>

This repository includes the data reduction and processing for the VAMPIRES coronagraph inner working angles (IWA).

## Setup

You may need to install some dependencies to run
```
pip install astropy numpy pandas tqdm
```
as well as these dependencies for the notebook
```
pip install proplot scipy
```

## Layout

### Data
Raw data is sym-linked under `data/`
* `data/darks`
* `data/clc2`
* `data/clc3`
* `data/clc5`
* `data/clc7`
* `data/dgvvc`

### Scripts
Scripts to process this data are  in `scripts/`

* `scripts/reduce.py` takes each input file and dark-subtracts and collapses with error propagation
* `scripts/make_table.py` takes collapsed data and creates a table with the source fiber x and y positions along with the total sum of the collapsed frame with error propagation.

### Notebooks
A notebook with some processing and plotting is included in the `notebooks/` directory.

### Figures
The processing notebook ouotputs plot figures into the `figures/` directory.
