from astropy.io import fits
import tqdm.auto as tqdm
from pathlib import Path
import numpy as np
import argparse
import pandas as pd

def get_statistics(path: Path) -> dict:
    with fits.open(path) as hdul:
        data = hdul[0].data
        err = hdul["ERR"].data
        header = hdul[0].header
    
    total = np.sum(data)
    total_err = np.sqrt(np.sum(err**2))
    x_zp = 7.7 # zero point for x stage
    y_zp = 23.15 # zero point for y stage
    return {
        "x": header["X_SRCFIX"] - x_zp,
        "y": header["X_SRCFIP"] - y_zp,
        "total": total,
        "totalerr": total_err
    }

parser = argparse.ArgumentParser()
parser.add_argument("filenames", nargs="*", type=Path)
parser.add_argument("-o", "--output", help="output csv name", type=Path)

def main():
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pbar = tqdm.tqdm(args.filenames, desc="Creating table")
    rows = [get_statistics(path) for path in pbar]
    table = pd.DataFrame(rows)
    table.to_csv(args.output)

if __name__ == "__main__":
    main()
