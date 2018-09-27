from pathlib import Path
import tarfile

# parameters
input_folder = 'data/raw/'
output_folder = 'data/extracted/'

# get gzipped files
p = Path(input_folder).glob('*')
files = [x for x in p if x.is_file() and x.suffix == '.gz']

# extract them
for file in files:
    tar = tarfile.open(file, "r:gz")
    tar.extractall(path=output_folder)
    tar.close()
