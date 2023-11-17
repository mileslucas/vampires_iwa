from astropy.io import fits
import tqdm.auto as tqdm
from pathlib import Path
import numpy as np
import argparse

def make_dark(path: Path):
    data, header = fits.getdata(path, header=True)
    coll_data = np.mean(data, axis=0)
    coll_err = np.std(data, axis=0)
    coll_err += coll_err / np.sqrt(data.shape[0])
    dark_hdul = fits.HDUList([
        fits.PrimaryHDU(coll_data, header),
        fits.ImageHDU(coll_err, header, name="ERR")
    ])
    return dark_hdul

def calibrate_file(path: Path, dark_hdul: fits.HDUList, outpath: Path) -> Path:
    if outpath.is_file():
        return outpath

    data, header = fits.getdata(path, header=True)

    calib_data = data - dark_hdul[0].data
    coll_data = np.mean(calib_data, axis=0)
    cube_err = dark_hdul["ERR"].data**2 + np.maximum(calib_data / header["GAIN"], 0)
    coll_err = np.sqrt(np.mean(cube_err, axis=0) / cube_err.shape[0])

    hdul = fits.HDUList([
        fits.PrimaryHDU(coll_data, header),
        fits.ImageHDU(coll_err, header, name="ERR")
    ])

    hdul.writeto(outpath, overwrite=True)

    return outpath

parser = argparse.ArgumentParser()
parser.add_argument("filenames", nargs="*", type=Path)
parser.add_argument("-d", "--dark", help="dark file", type=Path)
parser.add_argument("-o", "--output", help="output directory", type=Path)

def main():
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    dark_hdul = make_dark(args.dark)
    for path in tqdm.tqdm(args.filenames, desc="Reducing data"):
        outpath = args.output / path.name.replace(".fits", "_coll.fits")
        calibrate_file(path, dark_hdul, outpath=outpath)

if __name__ == "__main__":
    main()
