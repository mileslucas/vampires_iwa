from pathlib import Path

rootdir = Path(__file__).parent.parent.resolve().absolute()

datadir = rootdir / "data"
notebookdir = rootdir / "notebooks"
scriptdir = rootdir / "scripts"
figdir = rootdir / "figures"
figdir.mkdir(exist_ok=True)
