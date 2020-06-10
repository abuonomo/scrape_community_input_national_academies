# Download files from the community input table csv
# author: Anthony Buonomo
# email: arb246@georgetown.edu

import argparse
import logging
from pathlib import Path
import os

import requests
import pandas as pd
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def main(infile: os.PathLike, outdir: Path):
    df = pd.read_csv(infile, index_col=0)
    filenames = df['FileName'].tolist()
    urls = df['FileUrl'].tolist()
    progress_bar = tqdm(zip(urls, filenames), total=len(urls))

    outdir.mkdir()
    for url, filename in progress_bar:
        progress_bar.set_description(filename)
        res = requests.get(url, allow_redirects=True)
        import ipdb; ipdb.set_trace()   
        with open(outdir / filename, 'wb') as f0:
            f0.write(res.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Download pdf files given csv with urls and filenames')
    parser.add_argument('i', help='input csv of filenames and urls', type=Path)
    parser.add_argument('o', help='output directory for the papers', type=Path)
    args = parser.parse_args()
    main(args.i, args.o)
